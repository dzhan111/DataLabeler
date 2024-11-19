from src.qc import QualityControl
import os
from cerebras.cloud.sdk import Cerebras
from typing import List

client = Cerebras(
    # This is the default and can be omitted
    api_key = os.environ.get('CEREBRAS_API_KEY'),
)

class Aggregation:
    def __init__(self, image_path):
        self.image_path = image_path
        self.qc = QualityControl(image_path, 80)
        self.valid_transcriptions = []

    def check(self):
        return len(self.valid_transcriptions) >= 3

    def process_transcription(self, transcription):
        if self.qc.fits_quality_control(transcription):
            self.valid_transcriptions.append(transcription)
    
    def aggregate(self):
        n = len(self.valid_transcriptions)
        joined = "\n".join([f"Caption {i + 1}: {x}" for i, x in enumerate(self.valid_transcriptions)])
        message_prompt = f"Your job is to combine the following {n} image captions, keeping as much information as possible from each but also keeping information consistent (there may be errors in each): {joined}"
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_prompt
                },
            ],
            model="llama3.1-8b",
            max_tokens=8192,
        )
        result_one = chat_completion.choices[0].message.content
        result_two = chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_prompt
                },
                {
                    "role": "assistant",
                    "content": result_one
                },
                {
                    "role": "user",
                    "content": "Now refine the wording so it is more logical."
                },
            ],
            model="llama3.1-8b",
            max_tokens=8192,
        ).choices[0].message.content
        return result_two
