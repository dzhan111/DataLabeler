from pathlib import Path
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from typing import Dict
import os
import random

from src.image_utils import load_images
from src.clients import WHISPER_MODEL

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware, 
    allow_origins = origins, 
    allow_credentials = True,
    allow_methods=['*'],
    allow_headers=['*']
)

# Initialize
transcriptions = {}

# Load images into Aggregation objects, convert them to .jpeg first if needed
images = load_images('data/dataset')

class ImageResponse(BaseModel):
    index: int
    api_image_url: str
    image_path: str

@app.get("/generate_image", response_model=ImageResponse)
async def generate_image():
    """Endpoint to return a random image index and its temporary URL."""
    if not images:
        raise HTTPException(status_code=404, detail="No images available")
    ind = random.randint(0, len(images) - 1)
    image_path = images[ind].image_path
    return ImageResponse(
        index=ind,
        image_path=image_path,
        api_image_url=f"/image/{ind}"  # A secondary endpoint to fetch the image
    )

@app.get("/image/{image_index}")
async def serve_image(image_index: int):
    """Endpoint to serve an image file by index."""
    if not images or image_index < 0 or image_index >= len(images):
        raise HTTPException(status_code=404, detail="Image not found")
    return FileResponse(images[image_index].image_path, media_type="image/jpeg")


@app.post("/process_audio/{ind}")
async def process_audio(ind: int, audio_file: UploadFile = File(...)):
    """Endpoint to process audio with Whisper model and update the Aggregation object."""
    if ind < 0 or ind >= len(images):
        raise HTTPException(status_code=404, detail="Invalid image index")
    
    agg_object = images[ind]
    
    # Save uploaded audio file temporarily for transcription
    temp_audio_path = f"./temp_{audio_file.filename}.webm"
    with open(temp_audio_path, "wb") as f:
        f.write(await audio_file.read())
    
    # Transcribe audio
    try:
        result = WHISPER_MODEL.transcribe(str(Path(temp_audio_path).absolute()))['text']
    finally:
        os.remove(str(Path(temp_audio_path).absolute()))
    
    # Process transcription
    add = agg_object.process_transcription(result)
    if add:
        #add confirmation code to DB and return a valid code
        pass
    if agg_object.check():
        final_transcription = agg_object.aggregate()
        transcriptions[final_transcription] = agg_object
        images.pop(ind)
    
    return {"message": "Audio processed successfully", "transcription": result}


@app.get("/transcriptions", response_model=Dict[str, str])
async def get_transcriptions():
    """Endpoint to retrieve all final transcriptions."""
    return {key: agg_object.path for key, agg_object in transcriptions.items()}

# Need endpoint to get if a confirmation code and worker_id combo is valid
# Use this for the front-end to see if they should display a code and if not allow re-record
# Need this for Mturk to see if they should get paid

@app.get("/code", response_model=bool)
async def is_code_valid(worker_id: int, code: int):
    #query db to check for code
    return False