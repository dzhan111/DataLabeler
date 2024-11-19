from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
import random

from src.image_utils import load_images
from src.clients import WHISPER_MODEL

app = FastAPI()

# Initialize
transcriptions = {}

# Load images into Aggregation objects, convert them to .jpeg first if needed
images = load_images('data/dataset')

class ImageResponse(BaseModel):
    index: int
    image_path: str

@app.get("/generate_image", response_model=ImageResponse)
async def generate_image():
    """Endpoint to return a random image index and path."""
    if not images:
        raise HTTPException(status_code=404, detail="No images available")
    ind = random.randint(0, len(images) - 1)
    return ImageResponse(index=ind, image_path=images[ind].image_path)


@app.post("/process_audio/{ind}")
async def process_audio(ind: int, audio_file: UploadFile = File(...)):
    """Endpoint to process audio with Whisper model and update the Aggregation object."""
    if ind < 0 or ind >= len(images):
        raise HTTPException(status_code=404, detail="Invalid image index")
    
    agg_object = images[ind]
    
    # Save uploaded audio file temporarily for transcription
    temp_audio_path = f"temp_{audio_file.filename}"
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())
    
    # Transcribe audio
    try:
        result = WHISPER_MODEL.transcribe(temp_audio_path)['text']
    finally:
        os.remove(temp_audio_path)  # Clean up the temp file
    
    # Process transcription
    agg_object.process_transcription(result)
    if agg_object.check():
        final_transcription = agg_object.aggregate()
        transcriptions[final_transcription] = agg_object
        images.pop(ind)
    
    return {"message": "Audio processed successfully", "transcription": result}


@app.get("/transcriptions", response_model=Dict[str, str])
async def get_transcriptions():
    """Endpoint to retrieve all final transcriptions."""
    return {key: agg_object.path for key, agg_object in transcriptions.items()}