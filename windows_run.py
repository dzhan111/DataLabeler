import uvicorn

if __name__ == "__main__":
    uvicorn.run("src.routes:app", reload=True, host="127.0.0.1", port=8000, log_level="info")