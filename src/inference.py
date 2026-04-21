# ===================== IMPORTS =====================
import os
import json
import joblib
import numpy as np
from typing import Dict, Any, List

from config import PATH_CONFIG
from src.utils import setup_logger

# ===================== LOGGER =====================
logger = setup_logger("inference")

# ===================== CONSTANTS =====================
MODEL_PATH = PATH_CONFIG["model_path"]
METADATA_PATH = "models/model_metadata.json"

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

    def load_model(self):
        if not os.path.exists(self.model_path):
            logger.critical(f"Model not found at {self.model_path}")
            raise FileNotFoundError("Model file missing")

        try:
            self.model = joblib.load(self.model_path)
            logger.info("Model loaded successfully")

            # 🔥 DEFAULT FALLBACK (IMPORTANT)
            self.model_name = self.model.__class__.__name__

            # 🔥 OVERRIDE WITH METADATA IF AVAILABLE
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

                    logger.info(f"Model name loaded from metadata: {self.model_name}")

                except Exception as e:
                    logger.warning(f"Metadata read failed: {e}")
                    logger.info(f"Using fallback model name: {self.model_name}")

            else:
                logger.warning("Metadata file not found, using fallback model name")

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
        try:
            ordered = [float(features[f]) for f in FEATURE_ORDER]
            return np.array([ordered], dtype=np.float32)
        except Exception as e:
            raise ValueError(f"Feature conversion error: {e}")


# ===================== PREDICTION ENGINE =====================
class StegoPredictor:

    def __init__(self, model_path: str = MODEL_PATH):
        self.loader = ModelLoader(model_path)
        self.model = self.loader.get_model()
        self.model_name = self.loader.model_name

    def predict(self, features: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Validate features
            FeatureProcessor.validate_features(features)

            # Convert to numpy
            X = FeatureProcessor.to_numpy(features)

            # Model inference
            prediction = self.model.predict(X)[0]
            proba = self.model.predict_proba(X)[0]

            stego_prob = float(proba[1])
            clean_prob = float(proba[0])

            label = "Stego" if prediction == 1 else "Clean"

            # Risk logic
            if stego_prob < 0.4:
                risk = "Low"
                decision = "Confident Clean"
            elif stego_prob <= 0.6:
                risk = "Medium"
                decision = "Uncertain"
            else:
                risk = "High"
                decision = "Confident Stego"

            result = {
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

            logger.info(f"Inference successful → {result}")
            return result

        except Exception as e:
            logger.error(f"Inference failed: {e}")
            raise RuntimeError("Prediction failed")


# ===================== SINGLETON =====================
predictor = StegoPredictor()


# ===================== HELPER =====================
def run_inference(features: Dict[str, Any]) -> Dict[str, Any]:
    return predictor.predict(features)