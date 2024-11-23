# Backend
This is a FastAPI backend to connect our frontend to the following third-party services:
- Supabase
- Mega.io
- Mechanical Turk
- OpenAI GPT-4o
- Cerebras Llama-3.1b

## Running
1. Ensure you are in the root directory of the repo and that you have Python 3.11+ installed on your machine.
2. Install dependencies

    1. `python -m venv venv`

    2. Activate environment: 
        - **Linux/Mac:** `. venv/bin/activate`

        - **Windows (with quotes):** `"venv/Scripts/activate"`

    3. `pip install -r requirements.txt`

3. Set environment variables in .env file (see [example](../.env.example)). We recommend setting ENV_TYPE to `dev`.

4. Run the FastAPI server

    `python -m run`

5. Done! Your backend should be located at http://localhost:8000 for the dev environment.