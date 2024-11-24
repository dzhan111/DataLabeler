# Backend
This is a FastAPI backend to connect our frontend to the following third-party services:
- Supabase
- Mega.io
- Mechanical Turk
- OpenAI GPT-4o
- Cerebras Llama-3.1b

## Running Locally
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

5. Done! Your backend should be located at http://localhost:8000 for the dev environment. You can visit http://localhost:8000/docs for an interactive documentation.

## Deployment Notes

If you plan to deploy this to Render or another service, note the following:
- Add the .env file or set environment variables
- Set the ENV_TYPE to `prod` or something other than `dev` or `test`
- Add Python to the environment if not already present
- Set the build command to `pip install -r requirements.txt`
- Set the startup command to `python -m run`
- We have a keep_alive task that self-pings every 600 seconds (10 minutes) to prevent spinning down. You can adjust the timing based on the cloud platform [in the keep_alive function here](./routes.py)
- You can still visit the interactive docs at YOUR_URL/docs

## Files and Directories
### [scripts/](scripts/)
Contains the following scripts:
- [aggregation_tester.py](scripts/aggregation_tester.py): tests aggregation
- [hit_creator.py](scripts/hit_creator.py): creates HITs, or optionally deletes them
- [keyword_checker.py](scripts/keyword_checker.py): runs keyword checking flow
    - [script.txt](scripts/script.txt) is the input
- [populate_dbs.py](scripts/populate_dbs.py): adds images to DB in consistent way
- [syspathhack.py](scripts/syspathhack.py): allows imports from parent dir
### [agg.py](agg.py)
Aggregation logic for the app using LLama-3.1b
### [alock.py](alock.py)
Asynchronous locking for a shared resource
### [clients.py](clients.py)
Clients for accessing third-party services in a consistent manner
### [image_utils.py](image_utils.py)
Contains code to convert images to jpeg, the format we work with
### [mturk.py](mturk.py)
Handles the MTurk verification task as an asyncio task
### [qc.py](qc.py)
Checks keywords 
### [README.md](README.md)
More in-depth explanation of backend code
### [routes.py](routes.py)
Main FastAPI app code and route definitions