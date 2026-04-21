# 🚀 StegoAI – Demo Showcase

## 📌 Overview

This demo presents the **StegoAI API**, a production-grade system designed for **PDF steganalysis** using machine learning and forensic feature extraction.

The system detects hidden (covert) data embedded within PDF files by analyzing structural, statistical, and anomaly-based features.

---

## 🎯 Key Capabilities

* 🔍 Detect hidden data in PDF files
* 📊 Feature-based and file-based inference
* ⚡ Real-time API predictions
* 🧠 Explainable outputs (confidence, risk level, probabilities)
* 🛡️ Designed for digital forensics and cybersecurity use cases

---

## 🧪 Demo Endpoints

### 1️⃣ Feature-Based Prediction

* **Endpoint:** `/predict`
* **Input:** `sample_input.json`
* **Output:** `sample_output.json`

This mode allows direct testing using pre-extracted features.

---

### 2️⃣ PDF Upload Detection

* **Endpoint:** `/upload-pdf`
* **Input:** `sample_pdf/test.pdf`
* **Output:** JSON response with prediction and analysis

This demonstrates the **end-to-end pipeline**:

```
PDF → Feature Extraction → ML Model → Detection Output
```

---

## 📂 Demo Files

| File                       | Description              |
| -------------------------- | ------------------------ |
| `sample_input.json`        | Example feature input    |
| `sample_output.json`       | Example API response     |
| `sample_pdf/test.pdf`      | Sample PDF for testing   |
| `screenshots/api_demo.png` | Live API execution proof |

---

## 📊 Sample Output

```json
{
  "prediction": "Clean",
  "confidence": 0.4072,
  "risk_level": "Medium",
  "decision": "Uncertain (boundary case)",
  "model_used": "XGBoost",
  "probabilities": {
    "clean": 0.5928,
    "stego": 0.4072
  }
}
```

---

## 📸 API Demo

Refer to:

```
demo/screenshots/api_demo.png
```

This screenshot demonstrates:

* PDF upload via Swagger UI
* Real-time inference
* Structured response output

---

## 🧠 Technical Highlights

* Feature Engineering:

  * Entropy analysis
  * Structural anomaly detection
  * Metadata inspection

* Models Used:

  * Random Forest
  * XGBoost
  * LightGBM

* Best Model:

  * **XGBoost (based on F1-score and generalization)**

---

## 💡 Use Cases

* Digital Forensics Investigation
* Malware & Covert Channel Detection
* Secure Document Validation
* Cyber Threat Intelligence

---

## 🚀 Value Proposition

StegoAI provides a **scalable and extensible framework** for detecting hidden information across digital formats, with future scope for:

* Image steganalysis
* Audio/video covert detection
* Multi-modal security intelligence

---

## 🏁 Conclusion

This demo validates the **practical applicability** of StegoAI as a real-world cybersecurity tool, combining machine learning with forensic analysis for robust hidden data detection.

---
