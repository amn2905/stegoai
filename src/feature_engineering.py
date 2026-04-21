# ===================== IMPORTS =====================
import os
import numpy as np
from collections import Counter
from pypdf import PdfReader
from src.utils import setup_logger

logger = setup_logger("feature_engineering")


# ===================== HELPER FUNCTIONS =====================
def safe_text_extract(reader):
    text = ""
    try:
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted
    except Exception as e:
        logger.warning(f"Text extraction failed | {e}")
    return text


def compute_entropy(data: str):
    if not data:
        return 0.0
    counter = Counter(data)
    probs = [v / len(data) for v in counter.values()]
    return -sum(p * np.log2(p) for p in probs if p > 0)


def safe_div(a, b):
    return a / b if b != 0 else 0.0


# ===================== MAIN FEATURE EXTRACTION =====================
def extract_features_from_pdf(pdf_path):
    try:
        # ---------------- FILE LEVEL ----------------
        file_size = os.path.getsize(pdf_path)

        with open(pdf_path, "rb") as f:
            reader = PdfReader(f)
            pages = reader.pages

            num_pages = len(pages)
            object_count = num_pages
            avg_objects_per_page = safe_div(object_count, num_pages)

            # ---------------- TEXT ----------------
            text = safe_text_extract(reader)
            text_length = len(text)
            text_entropy = compute_entropy(text)

            invisible_text_ratio = safe_div(text.count(" "), text_length)

            # ---------------- METADATA ----------------
            metadata = reader.metadata
            metadata_str = str(metadata) if metadata else ""
            metadata_length = len(metadata_str)
            metadata_entropy = compute_entropy(metadata_str)

        # ---------------- STRUCTURAL ----------------
        with open(pdf_path, "rb") as f:
            raw_content = f.read().decode(errors="ignore")

        obj_count = raw_content.count("obj")
        stream_count = raw_content.count("stream")
        xref_count = raw_content.count("xref")

        structural_complexity_score = obj_count + stream_count + xref_count
        xref_gap_score = safe_div(xref_count, obj_count + 1)

        comment_length_ratio = safe_div(raw_content.count("%"), len(raw_content))
        padding_byte_ratio = safe_div(raw_content.count("\x00"), len(raw_content))

        # ---------------- IMAGE ----------------
        image_count = raw_content.count("/Image")

        # ---------------- FINAL FEATURE DICT ----------------
        features = {
            "file_size": float(file_size),
            "object_count": float(object_count),
            "avg_objects_per_page": float(avg_objects_per_page),
            "metadata_length": float(metadata_length),
            "metadata_value_entropy": float(metadata_entropy),
            "invisible_text_ratio": float(invisible_text_ratio),
            "avg_char_spacing_deviation": 0.0,
            "comment_length_ratio": float(comment_length_ratio),
            "xref_gap_score": float(xref_gap_score),
            "padding_byte_ratio": float(padding_byte_ratio),
            "image_count": float(image_count),
            "image_entropy_delta": 0.0,
            "image_size_anomaly": 0.0,
            "text_to_nontext_ratio": float(safe_div(text_length, len(raw_content))),
            "structural_complexity_score": float(structural_complexity_score)
        }

        logger.info(f"Features extracted successfully: {pdf_path}")
        return features

    except Exception as e:
        logger.error(f"Feature extraction failed: {pdf_path} | {e}")

        # FAIL-SAFE
        return {
            "file_size": 0.0,
            "object_count": 0.0,
            "avg_objects_per_page": 0.0,
            "metadata_length": 0.0,
            "metadata_value_entropy": 0.0,
            "invisible_text_ratio": 0.0,
            "avg_char_spacing_deviation": 0.0,
            "comment_length_ratio": 0.0,
            "xref_gap_score": 0.0,
            "padding_byte_ratio": 0.0,
            "image_count": 0.0,
            "image_entropy_delta": 0.0,
            "image_size_anomaly": 0.0,
            "text_to_nontext_ratio": 0.0,
            "structural_complexity_score": 0.0
        }