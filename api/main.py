# ===================== IMPORTS =====================
from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import numpy as np
import os
import uuid

from config import PATH_CONFIG, API_CONFIG
from src.utils import setup_logger
from src.feature_engineering import extract_features_from_pdf
from src.inference import run_inference

# ===================== LOGGER =====================
logger = setup_logger("api")

# ===================== CONSTANTS =====================
FEATURE_ORDER = [
    "file_size",
    "object_count",
    "avg_objects_per_page",
    "metadata_length",
    "metadata_value_entropy",
    "invisible_text_ratio",
    "avg_char_spacing_deviation",
    "comment_length_ratio",
    "xref_gap_score",
    "padding_byte_ratio",
    "image_count",
    "image_entropy_delta",
    "image_size_anomaly",
    "text_to_nontext_ratio",
    "structural_complexity_score"
]

# ===================== APP =====================
app = FastAPI(
    title="StegoAI API",
    description="Production-grade PDF Steganalysis API",
    version="4.0"
)

# ===================== SCHEMA =====================
class FeatureInput(BaseModel):
    file_size: float
    object_count: float
    avg_objects_per_page: float
    metadata_length: float
    metadata_value_entropy: float
    invisible_text_ratio: float
    avg_char_spacing_deviation: float
    comment_length_ratio: float
    xref_gap_score: float
    padding_byte_ratio: float
    image_count: float
    image_entropy_delta: float
    image_size_anomaly: float
    text_to_nontext_ratio: float
    structural_complexity_score: float


# ===================== HEALTH =====================
@app.get("/")
def health():
    return {
        "status": "ok",
        "service": "StegoAI",
        "version": "4.0"
    }


# ===================== FEATURE INPUT =====================
@app.post("/predict")
def predict(data: FeatureInput):
    try:
        features_dict = data.dict()

        result = run_inference(features_dict)

        logger.info(f"Manual Prediction → {result}")
        return result

    except Exception as e:
        logger.error(f"Predict error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===================== PDF UPLOAD =====================
@app.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    temp_path = None

    try:
        # Validate file
        if not file.filename.lower().endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF files allowed")

        # File size check
        max_size = API_CONFIG["max_file_size_mb"] * 1024 * 1024
        content = await file.read()

        if len(content) > max_size:
            raise HTTPException(status_code=400, detail="File too large")

        # Save temp file
        temp_path = f"temp_{uuid.uuid4().hex}.pdf"

        with open(temp_path, "wb") as f:
            f.write(content)

        # Extract features
        features_dict = extract_features_from_pdf(temp_path)

        # Inference
        result = run_inference(features_dict)

        logger.info(f"PDF Prediction: {file.filename} → {result}")

        return {
            "file_name": file.filename,
            "result": result
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PDF error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)


# ===================== MODEL INFO =====================
@app.get("/model-info")
def model_info():
    return {
        "model_path": PATH_CONFIG["model_path"],
        "features": len(FEATURE_ORDER),
        "status": "production"
    }