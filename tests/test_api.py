# ===================== IMPORTS =====================
import sys
import os
import pytest
from fastapi.testclient import TestClient

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app

# ===================== FIXTURES =====================
@pytest.fixture(scope="module")
def client():
    return TestClient(app)


# ===================== TEST: HEALTH =====================
def test_health(client):
    response = client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "service" in data


# ===================== TEST: MODEL INFO =====================
def test_model_info(client):
    response = client.get("/model-info")
    assert response.status_code == 200

    data = response.json()
    assert "model" in data
    assert "features" in data
    assert data["features"] > 0


# ===================== TEST: PREDICT VALID =====================
def test_predict_valid(client):
    payload = {
        "file_size": 120000,
        "object_count": 45,
        "avg_objects_per_page": 3.5,
        "metadata_length": 200,
        "metadata_value_entropy": 4.2,
        "invisible_text_ratio": 0.02,
        "avg_char_spacing_deviation": 0.5,
        "comment_length_ratio": 0.01,
        "xref_gap_score": 0.3,
        "padding_byte_ratio": 0.05,
        "image_count": 2,
        "image_entropy_delta": 0.8,
        "image_size_anomaly": 0.1,
        "text_to_nontext_ratio": 0.7,
        "structural_complexity_score": 0.6
    }

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()

    assert data["prediction"] in ["Clean", "Stego"]
    assert 0.0 <= data["confidence"] <= 1.0
    assert data["risk_level"] in ["Low", "Medium", "High"]


# ===================== TEST: PREDICT INVALID =====================
def test_predict_invalid(client):
    response = client.post("/predict", json={})
    assert response.status_code == 422


# ===================== TEST: PDF UPLOAD =====================
def test_upload_pdf(client):
    pdf_path = os.path.join("demo", "sample_pdf", "test.pdf")

    assert os.path.exists(pdf_path), "Sample PDF not found!"

    with open(pdf_path, "rb") as f:
        response = client.post(
            "/upload-pdf",
            files={"file": ("test.pdf", f, "application/pdf")}
        )

    assert response.status_code == 200

    data = response.json()
    assert "file_name" in data
    assert "result" in data
    assert data["result"]["prediction"] in ["Clean", "Stego"]


# ===================== TEST: INVALID FILE =====================
def test_upload_invalid_file(client):
    response = client.post(
        "/upload-pdf",
        files={"file": ("test.txt", b"fake content", "text/plain")}
    )

    assert response.status_code == 400