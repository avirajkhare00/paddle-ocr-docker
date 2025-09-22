import io
import base64
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from paddleocr import PaddleOCR
from PIL import Image
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Plasho PaddleOCR Service",
             description="GPU-powered OCR service using PaddleOCR")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Modify this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize PaddleOCR with GPU support
try:
    ocr = PaddleOCR(use_angle_cls=True, lang='en')
    logger.info("PaddleOCR initialized successfully with GPU support")
except Exception as e:
    logger.error(f"Failed to initialize PaddleOCR: {str(e)}")
    raise

@app.get("/")
def read_root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "PaddleOCR GPU Service",
        "version": "1.0.0"
    }

@app.post("/ocr")
async def perform_ocr(file: UploadFile = File(...)):
    """
    Perform OCR on an uploaded image file
    """
    try:
        # Read the image file
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Perform OCR
        logger.info(f"Processing image: {file.filename}")
        result = ocr.ocr(image)
        
        # Format results
        formatted_result = []
        for line in result:
            for word_info in line:
                coords, (text, confidence) = word_info
                formatted_result.append({
                    "text": text,
                    "confidence": float(confidence),
                    "coordinates": coords
                })
        
        logger.info(f"Successfully processed image: {file.filename}")
        return {
            "filename": file.filename,
            "results": formatted_result
        }
    except Exception as e:
        logger.error(f"Error processing image {file.filename}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/ocr/base64")
async def perform_ocr_base64(data: dict):
    """
    Perform OCR on a base64 encoded image
    """
    try:
        if "image" not in data:
            raise HTTPException(status_code=400, detail="No image data provided")
            
        # Decode base64 image
        image_data = base64.b64decode(data["image"])
        image = Image.open(io.BytesIO(image_data))
        
        # Perform OCR
        logger.info("Processing base64 image")
        result = ocr.ocr(image)
        
        # Format results
        formatted_result = []
        for line in result:
            for word_info in line:
                coords, (text, confidence) = word_info
                formatted_result.append({
                    "text": text,
                    "confidence": float(confidence),
                    "coordinates": coords
                })
        
        logger.info("Successfully processed base64 image")
        return {"results": formatted_result}
    except Exception as e:
        logger.error(f"Error processing base64 image: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    """
    Detailed health check endpoint
    """
    return {
        "status": "healthy",
        "gpu": True,
        "service": "PaddleOCR",
        "version": "1.0.0",
        "endpoints": [
            {"path": "/", "method": "GET", "description": "Root endpoint"},
            {"path": "/ocr", "method": "POST", "description": "File upload OCR"},
            {"path": "/ocr/base64", "method": "POST", "description": "Base64 image OCR"},
            {"path": "/health", "method": "GET", "description": "Health check"}
        ]
    }
