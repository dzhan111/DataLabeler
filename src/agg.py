from src.qc import QualityControl
from src.clients import CEREBRAS_CLIENT

class Aggregation:
    def __init__(self, image_path, qc: QualityControl):
        self.image_path = image_path
        self.qc = qc
        self.valid_transcriptions = []

    def check(self) -> bool:
        return len(self.valid_transcriptions) >= 3

    def process_transcription(self, transcription) -> None:
        if self.qc.fits_quality_control(transcription):
            self.valid_transcriptions.append(transcription)
    
    def aggregate(self) -> str:
        if not self.check():
            raise ValueError(f'Not enough transcriptions ({len(self.valid_transcriptions)})')
        n = len(self.valid_transcriptions)
        joined = "\n".join([f"Caption {i + 1}: {x}\n" for i, x in enumerate(self.valid_transcriptions)])
        message_prompt = f"""Your job is to combine the following {n} image captions into 1 unified description capturing all of the information in each.
        Please do your best to keep as many of the details as possible while maintaining consistency of the scene.
        Remove phrases and words that do not make sense in the context provided by the responses. Please do not report anything else. Only return the description.
        {joined}
        Please provide the resulting description in your following message:"""
        chat_completion = CEREBRAS_CLIENT.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": message_prompt
                },
            ],
            model="llama3.1-8b",
            max_tokens=8192,
        )
        result = chat_completion.choices[0].message.content
        return result
