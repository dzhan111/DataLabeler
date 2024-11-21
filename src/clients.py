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

class MockModel:
    def __init__(self):
        pass
    def transcribe(self, _):
        return {"text": "There is a man walking two dogs in a city park and it appears to be the middle of winter. One of the dogs is a small and black. The other one is a golden retriever. The person is wearing a grey hat and a scarf around. There knows a black coat, gloves and what appears to be snow pants. The city in the background is very consists of 10 buildings and there are park benches on the right side of the walkway. The ground is covered in snow and there is a pigeon standing in the middle of the walkway. The trees, there are trees in the background which all don't have leaves."}
WHISPER_MODEL = MockModel()
match os.environ.get('ENV_TYPE'):
    case "dev":
        pass
    case "test":
        WHISPER_MODEL = whisper.load_model('tiny.en')
    case _:
        WHISPER_MODEL = whisper.load_model('tiny.en')

MEGA_CLIENT = Mega().login(
    os.environ.get('MEGA_USER'),
    os.environ.get('MEGA_PASSWORD')
)

SUPABASE_CLIENT: Client = create_client(
    os.environ.get('SUPABASE_URL'),
    os.environ.get('SUPABASE_ADMIN_KEY')
)