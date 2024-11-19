import os
from openai import OpenAI
from cerebras.cloud.sdk import Cerebras
import whisper
from dotenv import load_dotenv

load_dotenv('.env')

OPENAI_CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CEREBRAS_CLIENT = Cerebras(api_key = os.environ.get('CEREBRAS_API_KEY'))

WHISPER_MODEL = whisper.load_model("tiny.en" if os.environ.get('ENV_TYPE') == 'dev' else 'base.en')