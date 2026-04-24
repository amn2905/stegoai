# 🚀 StegoAI – Demo Showcase

## 📌 Overview

**StegoAI** is a production-oriented API system for **PDF steganalysis**, leveraging machine learning and forensic feature engineering to detect hidden (covert) data within documents.

It analyzes structural patterns, statistical irregularities, and embedded anomalies to classify PDFs as **clean or stego-compromised**.

---

## 🎯 Key Capabilities

* 🔍 Detect hidden data in PDF files
* 📊 Support both feature-based and file-based inference
* ⚡ Real-time API predictions
* 🧠 Explainable outputs (confidence, probabilities, risk level)
* 🛡️ Designed for cybersecurity and digital forensics workflows

---

## 🧪 Demo Endpoints

### 1️⃣ Feature-Based Prediction

* **Endpoint:** `/predict`
* **Input:** `sample_input.json`
* **Output:** `sample_output.json`

Direct inference using pre-extracted features.

---

### 2️⃣ PDF Upload Detection

* **Endpoint:** `/upload-pdf`
* **Input:** `sample_pdf/test.pdf`
* **Output:** JSON response with prediction

**Pipeline:**

```
PDF → Feature Extraction → ML Model → Detection Output
```

---

## 📂 Demo Files

| File                  | Description           |
| --------------------- | --------------------- |
| `sample_input.json`   | Example feature input |
| `sample_output.json`  | API response output   |
| `sample_pdf/test.pdf` | Sample test document  |
| `demo/screenshots/`   | API demo screenshots  |

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
## 📸 User Interface (UI) Demo

The following screenshots demonstrate the **end-to-end user workflow** of StegoAI, from PDF upload to final analysis results.

### 📂 Screenshots Directory

```bash
demo/screenshots/
```

### 🖥️ UI Workflow Overview

| Screenshot                 | Description                                                           |
| -------------------------- | --------------------------------------------------------------------- |
| `demo_homepage.png`        | Landing page with system overview and navigation                      |
| `demo_upload.png`          | Interface for uploading PDF files for analysis                        |
| `demo_result.png`          | Prediction summary showing classification, confidence, and risk level |
| `demo_complete_result.png` | Detailed analysis report with extracted features and insights         |

---

### 🔄 End-to-End Flow

```bash
Upload PDF → Analyze → Prediction → Detailed Report
```

---
### 🎯 Highlights

* Clean and intuitive UI for seamless interaction
* Real-time processing and result visualization
* Structured output with explainable insights
* Designed for practical cybersecurity workflows

---

## 🧠 Technical Highlights

### Feature Engineering

* Entropy analysis
* Structural anomaly detection
* Metadata inspection

### Models Evaluated

* Random Forest
* XGBoost
* LightGBM

### Best Model

* **XGBoost** (based on F1-score and generalization performance)

---

## 💡 Use Cases

* Digital Forensics Investigation
* Malware & Covert Channel Detection
* Secure Document Validation
* Cyber Threat Intelligence

---

## 🚀 Value Proposition

StegoAI provides a **scalable and extensible framework** for hidden data detection in digital documents.

**Future Scope:**

* Image steganalysis
* Audio/Video covert detection
* Multi-modal security intelligence

---

## 🏁 Conclusion

This demo demonstrates the real-world applicability of **StegoAI** as a cybersecurity tool, combining machine learning with forensic analysis to deliver robust and explainable steganography detection.
