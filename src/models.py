from pydantic import BaseModel

class ImageTaskResponse(BaseModel):
    image_id: str

class AudioProcessResponse(BaseModel):
    accepted: bool
    payload: str