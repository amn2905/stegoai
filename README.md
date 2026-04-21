# 🔍 StegoAI – Production-Grade PDF Steganalysis Platform

## 📌 Overview

**StegoAI** is a production-grade, end-to-end **machine learning system for detecting hidden (covert) data within PDF files**. 

It integrates **digital forensics, advanced feature engineering, and ensemble learning models** to identify steganographic manipulation embedded deep within document structures.

The platform is engineered for **cybersecurity, digital forensics, and threat intelligence environments**, where traditional detection systems fail to identify concealed payloads.

---

## 🚨 Problem Statement

Modern steganography enables adversaries to hide sensitive or malicious data inside seemingly benign documents such as PDFs. 

This introduces critical risks across:

* 🔐 Data exfiltration
* 🕵️ Cybercrime investigations
* 🧾 Document-based malware delivery
* 🛡️ Enterprise security pipelines

Conventional antivirus and scanning tools primarily rely on signatures and **fail to detect structural-level hidden data**, making advanced steganalysis essential.

---

## 💡 Solution

StegoAI implements a **forensic ML pipeline** that:

* Extracts **high-dimensional structural and statistical features**
* Identifies anomalies in:

  * PDF structure
  * Metadata entropy
  * Hidden/invisible text patterns
  * Binary padding behavior
* Classifies documents into:

  * ✅ **Clean (Cover)**
  * ⚠️ **Stego (Hidden Data)**

---

## ⚙️ Key Capabilities

* 🧠 **Ensemble ML Architecture**
  Random Forest, XGBoost, and LightGBM (optimized via Optuna)

* 🔍 **Forensic Feature Engineering**
  Entropy modeling, XREF inconsistencies, padding anomalies, Unicode injection detection

* 📊 **Robust Evaluation Framework**
  Cross-validation, confusion matrices, ROC analysis

* 🚀 **Production API Layer (FastAPI)**
  Real-time inference via REST endpoints

* 📁 **Experiment Tracking & Reproducibility**
  Structured logging and JSON-based experiment storage

* 🛡️ **Security-Centric Design**
  Built for adversarial and real-world forensic environments

---

## 🧠 System Architecture

```text
PDF Input
   ↓
Forensic Feature Extraction
   ↓
ML Pipeline (RF / XGB / LGBM)
   ↓
Prediction Engine
   ↓
API Response (Confidence + Risk Analysis)
```

📄 Detailed architecture: `docs/architecture.md`

---

## 📊 Model Performance

| Model         | Accuracy | Precision | Recall   | F1 Score |
| ------------- | -------- | --------- | -------- | -------- |
| Random Forest | 0.79     | 0.79      | 0.79     | 0.79     |
| XGBoost       | 0.80     | 0.80      | 0.80     | 0.80     |
| LightGBM      | **0.81** | **0.81**  | **0.81** | **0.81** |

> 📌 **XGBoost selected for deployment** based on superior generalization and stability across validation folds.

---

## 📡 API Capabilities

### Core Endpoints

* `GET /` → Health check
* `POST /predict` → Feature-based classification
* `POST /upload-pdf` → Direct PDF steganalysis
* `GET /model-info` → Model metadata

### Sample Response

```json
{
  "file_name": "sample.pdf",
  "prediction": "Stego",
  "confidence": 0.82,
  "risk_level": "High",
  "probabilities": {
    "clean": 0.18,
    "stego": 0.82
  }
}
```

---

## 📁 Project Structure

```text
api/        → FastAPI service layer  
src/        → ML pipeline & feature engineering  
models/     → trained models  
results/    → metrics, logs, plots  
docs/       → architecture, dataset, features  
demo/       → sample inputs & outputs  
```

---

## 🧪 Dataset & Feature Engineering

* Custom-built **StegPDF dataset (~19K samples)**
* 8 steganography techniques × 3 payload intensities
* 21+ engineered features including:

  * Metadata entropy
  * Structural complexity
  * Padding ratios
  * Unicode injection patterns

📄 Documentation:

* `docs/dataset.md`
* `docs/features.md`

---

## 🛠️ Technology Stack

* **Language:** Python
* **Machine Learning:** Scikit-learn, XGBoost, LightGBM
* **API Framework:** FastAPI
* **Optimization:** Optuna
* **Data Processing:** Pandas, NumPy
* **Visualization:** Matplotlib, Seaborn

---

## 🔐 Security Perspective

StegoAI is designed to:

* Detect **covert communication channels**
* Identify **structural anomalies instead of known signatures**
* Operate effectively in **adversarial and forensic scenarios**

---

## 📁 Demo

Refer to `/demo/` for:

* Sample PDFs
* API outputs
* UI / response screenshots

---

## 🤝 Collaboration & Funding

The complete system (including full dataset, optimized models, and extended detection modules) is available for:

* Research collaboration
* Cybersecurity product integration
* Funding and deployment partnerships

📩 Contact: **[hamidamaan3@gmail.com](mailto:hamidamaan3@gmail.com)**

---

## 📈 Future Roadmap

* Multi-format steganalysis (Image, Audio, Video)
* Deep learning-based detection models
* Real-time streaming analysis
* Integration with SIEM / forensic platforms

---

## 📜 License

All Rights Reserved.
Unauthorized use, reproduction, or distribution is strictly prohibited.

---

## 🧠 Closing Statement

StegoAI is not merely a model—it is a **comprehensive steganalysis framework**, combining machine learning and digital forensics to detect hidden data at scale with production readiness.
