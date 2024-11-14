from fastapi import FastAPI, File, UploadFile, HTTPException
from pydantic import BaseModel
from typing import Dict
import os
import random
from agg import Aggregation
import whisper
from PIL import Image
from io import BytesIO
import base64

app = FastAPI()

# Initialize
folder_path = '../data/dataset'
images = []
whisper_model = whisper.load_model("base")
transcriptions = {}


def convert_to_jpeg(image_path: str) -> str:
    """Convert image to .jpeg format if it's a .jpg or .png."""
    if image_path.lower().endswith(('.jpg')):
        if os.path.exists(image_path.replace('.jpg', '.jpeg')):
            os.remove(image_path)
            return "removed"
        with Image.open(image_path) as img:
            # Create new path with .jpeg extension
            new_image_path = image_path.rsplit('.', 1)[0] + '.jpeg'
            img.save(new_image_path, 'JPEG')
            os.remove(image_path)
            return new_image_path
        os.remove(image_path)
    return image_path

# Load images into Aggregation objects, convert them to .jpeg first if needed
print(f"Loading images from {folder_path}...")
for filename in os.listdir(folder_path):
    original_image_path = os.path.join(folder_path, filename)
    # Convert to .jpeg if it's a jpg or png
    if not original_image_path.lower().endswith(('.jpeg')):
        jpeg_image_path = convert_to_jpeg(original_image_path)
        if jpeg_image_path == "removed" or not jpeg_image_path.lower().endswith('.jpeg'):
            continue
        images.append(Aggregation(jpeg_image_path))
    else:
        images.append(Aggregation(original_image_path))


print(f"Loaded {len(images)} images.")
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
        result = whisper_model.transcribe(temp_audio_path)['text']
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