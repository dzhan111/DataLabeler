import axios from "axios";
import React, { useEffect, useRef, useState } from "react";
import { FaStopCircle } from "react-icons/fa";
import { GrMicrophone } from "react-icons/gr";
import ReactLoading from 'react-loading';



const BASE_URL = import.meta.env.VITE_BACKEND_URL

const CaptionPage = ({ mturkId , onReceive }) => {
  // State management
  const [image, setImage] = useState(null);
  
  const [usingRecorded, setUsingRecorded] = useState(true);
  const [audioFile, setAudioFile] = useState(null);
  const [recordedAudio, setRecordedAudio] = useState(null);
  const [audioUrl, setAudioUrl] = useState(null);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingDuration, setRecordingDuration] = useState(0);
  
  const [error, setError] = useState(null);
  const [isLoading, setIsLoading] = useState(false);

  // Refs
  const isFetched = useRef(false);
  const mediaRecorderRef = useRef(null);
  const audioPlayer = useRef(null);
  const recordingIntervalRef = useRef(null);

  useEffect(() => {
    if (!isFetched.current) {
      isFetched.current = true;
      fetchImage();
    }

    return () => {
      if (audioUrl) {
        URL.revokeObjectURL(audioUrl);
      }
      if (image?.imageUrl) {
        URL.revokeObjectURL(image.imageUrl);
      }
    };
  }, []);

  const fetchImage = async () => {
    setIsLoading(true);
    setError(null);
    try {
      const metadataResponse = await axios.get(`${BASE_URL}/get_image_task`, 
        { params: { mturkid: mturkId } }
      );
      const { image_id } = metadataResponse.data;

      const imageResponse = await axios.get(`${BASE_URL}/get_image/${image_id}`, {
        responseType: "blob",
      });
      const imageUrl = URL.createObjectURL(imageResponse.data);

      setImage({ image_id, imageUrl });
    } catch (error) {
      setError("Failed to fetch image. Please try again.");
      console.error("Error fetching image:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleAudioUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      setAudioFile(file);
      setAudioUrl(URL.createObjectURL(file));
    }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      mediaRecorderRef.current = new MediaRecorder(stream);
      const chunks = [];

      mediaRecorderRef.current.ondataavailable = (event) => {
        if (event.data.size > 0) {
          chunks.push(event.data);
        }
      };

      mediaRecorderRef.current.onstop = () => {
        const audioBlob = new Blob(chunks, { type: "audio/webm" });
        const url = URL.createObjectURL(audioBlob);
        setRecordedAudio(audioBlob);
        setAudioUrl(url);
        setRecordingDuration(0);
      };

      mediaRecorderRef.current.start();
      setIsRecording(true);
      setRecordingDuration(0);

      // Start timer
      recordingIntervalRef.current = setInterval(() => {
        setRecordingDuration(prev => prev + 1);
      }, 1000);
    } catch (error) {
      setError("Error accessing microphone. Please check permissions.");
      console.error("Error accessing microphone:", error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current?.state === "recording") {
      mediaRecorderRef.current.stop();
      mediaRecorderRef.current.stream.getTracks().forEach(track => track.stop());
      
      // Clear interval
      if (recordingIntervalRef.current) {
        clearInterval(recordingIntervalRef.current);
      }
    }
    setIsRecording(false);
  };

  const submitAudio = async (audio) => {
    if (!audio || !image) {
      setError("Please provide both image and audio.");
      return;
    }

    setIsLoading(true);
    setError(null);
    
    const formData = new FormData();
    formData.append("audio_file", audio);

    try {
      const response = await axios.post(
        `${BASE_URL}/process_audio/${image.image_id}`, 
        formData, {
          params: {mturkid: mturkId},
          headers: { "Content-Type": "multipart/form-data" },
      });

      console.log(response);

      if (response.data.accepted) {
        onReceive(response.data.payload);
      } else {
        setError(response.data.payload);
      }
    } catch (error) {
      setError("Failed to process audio. Please try again.");
      console.error("Error processing audio:", error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {mturkId && (
        <h1 className="text-2xl font-bold mb-6">MTurk ID: {mturkId}</h1>
      )}

      <div className="bg-white rounded-lg shadow-md p-6 items-center max-w-xxl space-y-6">
        <h2 className="text-xl font-semibold">Image Captioning Task</h2>
        <h2 className="text-m font-normal">Given the following image, talk about what you see in the image. Be as detailed as you choose, but be sure to talk for at least 60 seconds.</h2>

        {image && <img
          src={image.imageUrl}
          alt="Task"
          className="w-full max-w-2xl mx-auto rounded-lg shadow-md"
        />}
        {isLoading && <ReactLoading className="mx-auto max-w-xl justify-items-center py-14" type={"spinningBubbles"} color={"black"} height={'10%'} width={'10%'} />}

        {usingRecorded ? <div>
          <button className='rounded-l-md px-4 py-2 bg-gray-300 text-black justify-items-center'>Record Audio </button>
          <button 
            className='rounded-r-md bg-blue-50 py-2 px-4 hover:bg-gray-100'
            onClick={() => {setUsingRecorded(false)}}
          >
            Upload Audio
          </button>
        </div> : <div>
          <button 
            className='rounded-l-md bg-blue-50 py-2 px-4 hover:bg-blue-100'
            onClick={() => {setUsingRecorded(true)}}
          >
            Record Audio 

          </button>
          <button className='rounded-r-md px-4 py-2 bg-gray-300 text-black justify-items-center'>Upload Audio</button>
        </div>}

        {usingRecorded ? <div>
          <h3 className="text-lg font-medium mb-2">Record Audio </h3> 
          <button
            onClick={isRecording ? stopRecording : startRecording}
            className={`px-4 py-2 rounded-md text-white font-medium relative 
              ${isRecording
                ? 'bg-red-600 hover:bg-red-700 '
                : 'bg-blue-600 hover:bg-blue-700'
              } 
              transition-colors`}
          > 
          <span className="flow-root">
            {isRecording ? <FaStopCircle className="float-left" /> : <GrMicrophone className="float-left"/>}
            
          </span>
            
          </button>
          {isRecording && (
              <div className="flex size-9 float-right items-center px-6 align-left">
                <span className="animate-pulse mr-1 text-xs">●</span>
                <span className="text-xs">{recordingDuration}s</span>
              </div>
            )}
        </div>
        :
        <div>
          <h3 className="text-lg font-medium mb-2">Upload Audio</h3>
          <input
            type="file"
            accept="audio/*"
            onChange={handleAudioUpload}
            className="block w-full text-sm text-gray-500 file:mr-4 file:py-2 
                      file:px-4 file:rounded-md file:border-0 
                      file:font-semibold file:bg-blue-50 file:text-blue-700
                      hover:file:bg-blue-100"
          />
        </div>}

        {audioUrl && <div>
          <h3 className="text-lg font-medium mb-2">Preview Audio</h3>
          <audio
            ref={audioPlayer}
            controls
            src={audioUrl}
            className="w-full mb-4"
          />
          <button
            onClick={() => submitAudio(usingRecorded ? recordedAudio : audioFile)}
            disabled={isLoading}
            className="px-4 py-2 bg-blue-600 text-white rounded-md
                      hover:bg-blue-700 transition-colors
                      disabled:opacity-50 disabled:cursor-not-allowed"
          >
            Submit Audio
          </button>
        </div>}

        {error && <p className="bg-red-50 text-red-600 p-4 rounded-md">
          {error}
        </p>}
      </div>
    </div>
  );
};

export default CaptionPage;