import os
from PIL import Image
from typing import List

from src.agg import Aggregation
from src.qc import QualityControl

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

def load_images(folder_path: str) -> List[Aggregation]:

    print(f"Loading images from {folder_path}...")

    images = []

    for filename in os.listdir(folder_path):
        image_path = os.path.join(folder_path, filename)

        # convert images to jpeg
        if not image_path.lower().endswith(('.jpeg')):
            image_path = convert_to_jpeg(image_path)
            if image_path == "removed" or not image_path.lower().endswith('.jpeg'):
                continue

        qc_module = None
        keyword_file = os.path.join(os.path.splitext(image_path)[0]) + '.txt'
        if os.path.isfile(keyword_file):
            keywords = []
            with open(keyword_file, 'r') as file:
                keywords = [i.strip() for i in file.readlines()]
            qc_module = QualityControl(image_path, keywords)
        else:
            print('miss')
            qc_module = QualityControl(image_path, [])
            with open(keyword_file, 'w') as file:
                for kw in qc_module.keywords:
                    file.write(kw + '\n')
        images.append(Aggregation(image_path, qc_module))

    print(f"Loaded {len(images)} images.")

    return images