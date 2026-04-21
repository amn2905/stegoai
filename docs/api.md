# 📡 StegoAI API Documentation

## 📌 Overview

StegoAI API provides endpoints for detecting hidden (steganographic) data in PDF files using machine learning models.

The API supports:

* Feature-based prediction
* Direct PDF file analysis
* Model metadata access

---

## 🌐 Base URL

```text
http://localhost:8000
```

---

## 🔍 Endpoints

---

## 1️⃣ Health Check

### `GET /`

Check if API is running.

### Response

```json
{
  "status": "ok",
  "service": "StegoAI",
  "version": "4.0"
}
```

---

## 2️⃣ Feature-Based Prediction

### `POST /predict`

Predict whether input features represent a **Clean** or **Stego** file.

### Request Body

```json
{
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
```

### Response

```json
{
  "prediction": "Stego",
  "confidence": 0.82,
  "risk_level": "High",
  "decision": "Confident Stego",
  "model_used": "XGBoost",
  "probabilities": {
    "clean": 0.18,
    "stego": 0.82
  }
}
```

---

## 3️⃣ PDF Upload (Recommended)

### `POST /upload-pdf`

Upload a PDF file directly for steganalysis.

### Request

* Content-Type: `multipart/form-data`
* File field: `file`

### Example (cURL)

```bash
curl -X POST "http://localhost:8000/upload-pdf" \
  -F "file=@test.pdf"
```

### Response

```json
{
  "file_name": "test.pdf",
  "result": {
    "prediction": "Clean",
    "confidence": 0.41,
    "risk_level": "Low",
    "decision": "Confident Clean"
  }
}
```

---

## 4️⃣ Model Information

### `GET /model-info`

Returns details about the deployed model.

### Response

```json
{
  "model_path": "models/best_model.pkl",
  "features": 15,
  "status": "production"
}
```

---

## ⚠️ Error Handling

| Status Code | Meaning                             |
| ----------- | ----------------------------------- |
| 400         | Invalid file (non-PDF or too large) |
| 422         | Invalid input format                |
| 500         | Internal server error               |

---

## 📦 File Upload Limits

* Allowed type: **PDF only**
* Max size: Defined in `.env` (`MAX_FILE_SIZE_MB`)

---

## 🧠 Prediction Logic

* Model: Ensemble (XGBoost / LightGBM / RandomForest)
* Output:

  * **Clean** → No hidden data detected
  * **Stego** → Possible hidden content detected

### Risk Levels

| Probability | Risk   |
| ----------- | ------ |
| < 0.4       | Low    |
| 0.4 – 0.6   | Medium |
| > 0.6       | High   |

---

## 🧪 Testing

Run tests using:

```bash
pytest
```

---

## 🐳 Docker Usage

### Build

```bash
docker build -t stegoai .
```

### Run

```bash
docker run -p 8000:8000 stegoai
```

---

## 📸 Demo

See `/demo/` folder for:

* Sample PDFs
* API responses
* Screenshots

---

## 🔐 Security Notes

* Do not expose `.env` publicly
* Validate file inputs before processing
* Use API keys for production (future scope)

---

## 🚀 Future Enhancements

* Authentication (API keys)
* Batch processing
* Multi-format steganalysis
* Real-time streaming detection

---

## 📩 Contact

For integration, deployment, or collaboration:

**Email:** [hamidamaan3@gmail.com](mailto:hamidamaan3@gmail.com)

---
