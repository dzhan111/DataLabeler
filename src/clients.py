import os
from openai import OpenAI
from cerebras.cloud.sdk import Cerebras
import whisper
from mega import Mega
from supabase import create_client, Client

from dotenv import load_dotenv

load_dotenv('.env')

OPENAI_CLIENT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

CEREBRAS_CLIENT = Cerebras(api_key = os.environ.get('CEREBRAS_API_KEY'))

WHISPER_MODEL = lambda _: "This is a sample transcription" 
if os.environ.get('ENV_TYPE') != 'dev':
    whisper.load_model('base.en')
    #whisper.load_model('tiny.en')

MEGA_CLIENT = Mega().login(
    os.environ.get('MEGA_USER'),
    os.environ.get('MEGA_PASSWORD')
)

SUPABASE_CLIENT: Client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_ADMIN_KEY')
)