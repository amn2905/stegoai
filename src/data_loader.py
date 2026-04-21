# ===================== IMPORTS =====================
import os
import numpy as np

from src.feature_engineering import extract_features_from_pdf
from src.utils import setup_logger

logger = setup_logger("data_loader")


# ===================== FEATURE ORDER =====================
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


# ===================== HELPER =====================
def dict_to_array(feature_dict):
    try:
        return [feature_dict[f] for f in FEATURE_ORDER]
    except KeyError as e:
        raise ValueError(f"Missing feature: {e}")


# ===================== LOAD DATASET =====================
def load_dataset(base_path):
    X, y = [], []

    logger.info(f"Loading dataset from: {base_path}")

    for label in ["cover", "stego"]:
        folder = os.path.join(base_path, label)

        if not os.path.exists(folder):
            logger.warning(f"Folder not found: {folder}")
            continue

        for file in os.listdir(folder):

            # Skip non-PDF
            if not file.lower().endswith(".pdf"):
                continue

            path = os.path.join(folder, file)

            try:
                features_dict = extract_features_from_pdf(path)
                features = dict_to_array(features_dict)

                X.append(features)
                y.append(0 if label == "cover" else 1)

            except Exception as e:
                logger.error(f"Error processing {file}: {e}")

    if len(X) == 0:
        raise ValueError("Dataset is empty. Check dataset path or feature extraction.")

    logger.info(f"Dataset loaded successfully: {len(X)} samples")

    return np.array(X, dtype=np.float32), np.array(y, dtype=np.int32)