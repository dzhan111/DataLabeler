import os
import random
from agg import Aggregation
import whisper

images = []
whisper_model = whisper.load_model("base")

"""
For each image_path in images create an aggregation object and add it to images
"""

folder_path = '../data/dataset'
transcriptions = {}

for filename in os.listdir(folder_path):
    images.append(Aggregation(os.path.join(folder_path, filename)))

def generate_image():
    ind = random.randint(0, len(images) - 1)
    return ind, images[ind]

def process_audio(ind, audio_file):
    agg_object = images[ind]
    result = whisper_model.transcribe(audio_file)['text']
    agg_object.process_transcription(result)
    if agg_object.check():
        final_transcription = agg_object.aggregate()
        transcriptions[final_transcription] = images[ind]
        images.pop(ind)







