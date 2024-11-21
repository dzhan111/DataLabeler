import uvicorn, os
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv('.env')
    if os.environ.get('ENV_TYPE') in ['dev', 'test']:
        uvicorn.run("src.routes:app", reload=True, host="127.0.0.1", port=8000, log_level="info")
    else:
        uvicorn.run("src.routes:app", host="0.0.0.0", port=10000, log_level="info")