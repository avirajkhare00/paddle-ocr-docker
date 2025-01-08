# Plasho PaddleOCR GPU Service

A GPU-powered OCR service using PaddleOCR with REST API endpoints.

## Features

- GPU-accelerated OCR processing
- REST API endpoints for file upload and base64 image processing
- Docker containerization with NVIDIA GPU support
- Detailed logging and error handling
- Health check endpoints
- CORS support

## Prerequisites

- NVIDIA GPU
- Docker with NVIDIA Container Toolkit
- Ubuntu 20.04 or later (for host system)

## Setup Instructions

1. Install NVIDIA Drivers and Docker:
```bash
# Install NVIDIA drivers
sudo apt-get update
sudo apt-get install -y nvidia-driver-525

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install NVIDIA Container Toolkit
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list
sudo apt-get update
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

2. Build and Run:
```bash
# Build Docker image
docker build -t plasho-paddleocr-gpu .

# Run container with GPU support
docker run --gpus all -p 8000:8000 plasho-paddleocr-gpu
```

## API Endpoints

1. Health Check
```
GET /
GET /health
```

2. File Upload OCR
```
POST /ocr
Content-Type: multipart/form-data
```

3. Base64 Image OCR
```
POST /ocr/base64
Content-Type: application/json
```

## Usage Examples

1. File Upload:
```python
import requests

url = "http://your-server:8000/ocr"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

2. Base64 Image:
```python
import requests
import base64

url = "http://your-server:8000/ocr/base64"
with open("image.jpg", "rb") as image_file:
    encoded_string = base64.b64encode(image_file.read()).decode()

data = {"image": encoded_string}
response = requests.post(url, json=data)
print(response.json())
```

## Response Format

```json
{
    "results": [
        {
            "text": "detected text",
            "confidence": 0.95,
            "coordinates": [[x1,y1], [x2,y2], [x3,y3], [x4,y4]]
        }
    ]
}
```

## Production Considerations

1. Security:
   - Implement authentication
   - Use HTTPS
   - Restrict CORS origins
   - Add rate limiting

2. Monitoring:
   - Set up proper logging
   - Monitor GPU usage
   - Track API performance

3. Maintenance:
   - Regular updates of CUDA drivers
   - Keep dependencies updated
   - Backup system

## Support

For issues and feature requests, please create an issue in the repository.
