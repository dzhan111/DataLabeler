from pydantic import BaseModel

class ImageTaskResponse(BaseModel):
    image_id: str