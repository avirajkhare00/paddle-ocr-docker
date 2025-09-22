# Use NVIDIA CUDA base image
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu20.04

# Set environment variables
ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/*

# Install PaddleOCR and its dependencies
RUN pip3 install --no-cache-dir \
    paddlepaddle-gpu \
    paddleocr \
    fastapi \
    uvicorn \
    python-multipart \
    pillow \
    backports.zoneinfo

# Create app directory
WORKDIR /app

# Copy application code
COPY ./app.py /app/
COPY ./requirements.txt /app/

# Expose port
EXPOSE 8000

# Run the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
