import os
from PIL import Image

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