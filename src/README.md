# Backend
This is a FastAPI backend to connect our frontend to the following third-party services:
- Supabase
- Mechanical Turk
- OpenAI GPT-4o
- Cerebras Llama-3.1b

## Running
1. Install dependencies
`pip install -r requirements.txt`
2. Run the FastAPI server

    Non-Windows: `uvicorn src.routes:app --reload`

    Goofy Ah Windows: `python -m windows_run`