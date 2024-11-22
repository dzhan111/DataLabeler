import os
from pathlib import Path

from dotenv import load_dotenv
import requests

from openai import OpenAI
from cerebras.cloud.sdk import Cerebras
from mega import Mega
from supabase import create_client, Client

load_dotenv('.env', override=True)

class Lemonfox_Client:
    URL: str = "https://api.lemonfox.ai/v1/audio/transcriptions"

    def __init__(self, api_key: str, logging_mode: bool):
        self.API_KEY = api_key
        self.HEADERS = {
            "Authorization": f"Bearer {api_key}"
        }
        self.logging_mode = logging_mode

    def transcribe(self, audio_file: str | Path) -> str:
        
        transcript = ''

        with open(audio_file, 'rb') as file:
            data = {
                "language": "english",
                "response_format": "json"
            }

            response = requests.post(
                self.URL, 
                headers=self.HEADERS, 
                files={'file': file}, 
                data=data
            )
            
            if response.ok:
                try:
                    transcript = response.json()['text']
                except KeyError as error:
                    print(error)

        if self.logging_mode:
            print('Transcript:', transcript)

        return transcript
    
OPENAI_CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CEREBRAS_CLIENT = Cerebras(api_key = os.environ.get('CEREBRAS_API_KEY'))

LEMONFOX_CLIENT = Lemonfox_Client(
    os.environ.get('LEMONFOX_KEY'),
    True if os.environ.get('ENV_TYPE') == 'dev' else False
)

MEGA_CLIENT = Mega().login(
    os.environ.get('MEGA_USER'),
    os.environ.get('MEGA_PASSWORD')
)

SUPABASE_CLIENT: Client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_ADMIN_KEY')
)