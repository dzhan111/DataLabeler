# production dockerfile

FROM ubuntu:22.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Clone the repository
RUN git clone https://github.com/dzhan111/DataLabeler.git .

RUN rm -rf ./frontend
RUN rm -rf ./assignments
RUN rm -rf ./data
RUN rm -rf ./docs
RUN rm README.md

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Expose FastAPI port
EXPOSE 10000

# Run FastAPI server
CMD ["uvicorn", "src.routes:app", "--host", "0.0.0.0", "--port", "10000"]