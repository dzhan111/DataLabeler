import React, { useState, useEffect } from "react";
import axios from "axios";
import { BASE_URL } from "./config";
import "./App.css";

function App() {
  const [image, setImage] = useState(null);
  const [audioFile, setAudioFile] = useState(null);
  const [allTranscriptions, setAllTranscriptions] = useState({});
  const [aggTranscriptions, setAggTranscriptions] = useState({});
  const [message, setMessage] = useState("");

  // Fetch a random image when the component mounts
  useEffect(() => {
    fetchImage();
  }, []);

  useEffect(() => {
    if (image) {
      fetchAllTranscriptions();
      fetchAggTranscriptions();
    }
  }, [image]);

  const fetchImage = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/generate_image`);
      setImage(response.data);
    } catch (error) {
      console.error("Error fetching image:", error);
    }
  };

  const handleAudioUpload = (event) => {
    setAudioFile(event.target.files[0]);
  };

  const submitAudio = async () => {
    if (!audioFile || !image) return;

    const formData = new FormData();
    formData.append("audio_file", audioFile);

    try {
      const response = await axios.post(`${BASE_URL}/process_audio/${image.index}`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      setMessage(response.data.message);
      fetchAggTranscriptions();
      fetchAllTranscriptions();
      // fetchImage(); // Load a new random image
    } catch (error) {
      console.error("Error processing audio:", error);
    }
  };

  const fetchAllTranscriptions = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/allValidTranscriptions`);
      let validTranscriptions = {};
      for (let key in response.data) {
        response.data[key] = response.data[key].split(" ")[0];
        if (response.data[key] === image.image_path) {
          validTranscriptions[key] = response.data[key];
        }
      }
      setAllTranscriptions(validTranscriptions);
    } catch (error) {
      console.error("Error fetching transcriptions:", error);
    }
  };

  const fetchAggTranscriptions = async () => {
    try {
      const response = await axios.get(`${BASE_URL}/aggTranscriptions`);
      let aggTranscriptionsDict = {};
      for (let key in response.data) {
        response.data[key] = response.data[key].split(" ")[0];
        if (key === image.image_path) {
          aggTranscriptionsDict[response.data[key]] = key;
        }
      }
      setAggTranscriptions(aggTranscriptionsDict);
    } catch (error) {
      console.error("Error fetching transcriptions:", error);
    }
  };


  return (
    <div className="App">
      <h1>Dwellify</h1>
      
      {image && (
        <div>
          {console.log(`${BASE_URL}/${image.image_path}`)}
          <h2>Current Image</h2>
          <img src={`${BASE_URL}/${image.image_path}`} alt="Random" width="300" />
        </div>
      )}

      <div>
        <h2>Upload Audio</h2>
        <input type="file" accept="audio/*" onChange={handleAudioUpload} />
        <button onClick={submitAudio} disabled={!audioFile}>Submit Audio</button>
      </div>

      {message && <p style={{ color: "green" }}>{message}</p>}

      <div>
        {allTranscriptions &&
        <>
          <h2>Valid Transcriptions</h2>
          <ol>
            {Object.entries(allTranscriptions).map(([text, path], idx) => (
              <li key={idx}>
                {`${BASE_URL}/${path}` === `${BASE_URL}/${image.image_path}` ?
                <>{text}</> : <></>}
              </li>
            ))}
          </ol>
        </>}
        {aggTranscriptions &&
        <>
          <h2>Aggregated Transcription</h2>
          <ol>
            {Object.entries(aggTranscriptions).map(([path, text], idx) => (
              <li key={idx}>
                {`${BASE_URL}/${path}` === `${BASE_URL}/${image.image_path}` ?
                <>{text}</> : <></>}
              </li>
            ))}
          </ol>
        </>}
      </div>
    </div>
  );
}

export default App;