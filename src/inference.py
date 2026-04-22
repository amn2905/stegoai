# ===================== IMPORTS =====================
import os
import json
import joblib
import numpy as np
import requests
from typing import Dict, Any, List

from config import PATH_CONFIG
from src.utils import setup_logger

# ===================== LOGGER =====================
logger = setup_logger("inference")

# ===================== CONSTANTS =====================
MODEL_PATH = PATH_CONFIG.get("model_path", "models/best_model.pkl")
METADATA_PATH = "models/model_metadata.json"

# 🔥 Google Drive Direct Link (converted)
MODEL_URL = os.getenv(
    "MODEL_URL",
    "https://drive.google.com/uc?export=download&id=1sLig5TaZXeAZyS_E7N3tpdcOxLiToyCE"
)

FEATURE_ORDER: List[str] = [
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


# ===================== MODEL LOADER =====================
class ModelLoader:

    def __init__(self, model_path: str = MODEL_PATH):
        self.model_path = model_path
        self.model = None
        self.model_name = "Unknown"

    def download_model(self):
        """Download model from Google Drive if not exists"""
        if os.path.exists(self.model_path):
            return

        try:
            logger.info("Downloading model from Google Drive...")

            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)

            response = requests.get(MODEL_URL)
            response.raise_for_status()

            with open(self.model_path, "wb") as f:
                f.write(response.content)

            logger.info("Model downloaded successfully")

        except Exception as e:
            logger.critical(f"Model download failed: {e}")
            raise RuntimeError("Model download error")

    def load_model(self):
        """Load model (download if missing)"""
        if not os.path.exists(self.model_path):
            self.download_model()

        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model file missing")

        try:
            self.model = joblib.load(self.model_path)
            logger.info("Model loaded successfully")

            # Default model name
            self.model_name = self.model.__class__.__name__

            # Metadata override
            if os.path.exists(METADATA_PATH):
                try:
                    with open(METADATA_PATH, "r") as f:
                        metadata = json.load(f)

                    self.model_name = metadata.get(
                        "model", {}
                    ).get(
                        "name",
                        metadata.get("best_model", self.model_name)
                    )

                except Exception as e:
                    logger.warning(f"Metadata read failed: {e}")

        except Exception as e:
            logger.critical(f"Model loading failed: {e}")
            raise RuntimeError("Model loading error")

    def get_model(self):
        if self.model is None:
            self.load_model()
        return self.model


# ===================== FEATURE PROCESSOR =====================
class FeatureProcessor:

    @staticmethod
    def validate_features(features: Dict[str, Any]) -> None:
        missing = [f for f in FEATURE_ORDER if f not in features]
        if missing:
            raise ValueError(f"Missing features: {missing}")

    @staticmethod
    def to_numpy(features: Dict[str, Any]) -> np.ndarray:
        ordered = [float(features[f]) for f in FEATURE_ORDER]
        return np.array([ordered], dtype=np.float32)


# ===================== PREDICTOR =====================
class StegoPredictor:

    def __init__(self, model_path: str = MODEL_PATH):
        self.loader = ModelLoader(model_path)
        self.model = None
        self.model_name = None

    def get_model(self):
        """Lazy load model"""
        if self.model is None:
            self.model = self.loader.get_model()
            self.model_name = self.loader.model_name
        return self.model

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        try:
            model = self.get_model()

            FeatureProcessor.validate_features(features)
            X = FeatureProcessor.to_numpy(features)

            prediction = model.predict(X)[0]
            proba = model.predict_proba(X)[0]

            stego_prob = float(proba[1])
            clean_prob = float(proba[0])

            label = "Stego" if prediction == 1 else "Clean"

            if stego_prob < 0.4:
                risk = "Low"
                decision = "Confident Clean"
            elif stego_prob <= 0.6:
                risk = "Medium"
                decision = "Uncertain"
            else:
                risk = "High"
                decision = "Confident Stego"

            return {
                "prediction": label,
                "confidence": round(stego_prob, 4),
                "risk_level": risk,
                "decision": decision,
                "model_used": self.model_name,
                "probabilities": {
                    "clean": round(clean_prob, 4),
                    "stego": round(stego_prob, 4)
                }
            }

        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise RuntimeError("Prediction failed")


# ===================== SINGLETON =====================
predictor = StegoPredictor()


# ===================== HELPER =====================
def run_inference(features: Dict[str, Any]) -> Dict[str, Any]:
    return predictor.predict(features)
