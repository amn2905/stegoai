# 🔍 StegoAI – PDF Steganalysis System

## 📌 Overview

**StegoAI** is a production-grade machine learning system designed to detect hidden (steganographic) data within PDF files.

It combines:

* 📊 Statistical feature engineering
* 🔍 Digital forensic analysis
* 🧠 Ensemble ML models (XGBoost, LightGBM, RandomForest)

This system is built for:

* Cybersecurity
* Digital forensics
* Threat detection

---

## 🚨 Problem Statement

Steganography allows attackers to embed hidden data inside seemingly harmless PDF files.

Traditional detection tools:

* ❌ Fail to detect hidden payloads
* ❌ Ignore structural anomalies

This leads to risks such as:

* Data exfiltration
* Malware delivery
* Covert communication

---

## 💡 Solution

StegoAI detects hidden data by:

* Extracting **structural + statistical features**
* Analyzing:

  * Metadata entropy
  * Invisible text patterns
  * Binary structure anomalies
* Classifying files as:

  * ✅ Clean
  * ⚠️ Stego

---

## ⚙️ Key Features

* 🧠 Ensemble ML models (RF, XGBoost, LightGBM)
* 🔍 Advanced feature engineering
* 📊 Model evaluation (Confusion Matrix, ROC)
* 🚀 FastAPI-based inference API
* 📁 Structured and scalable architecture

---

## 🧠 Architecture

```
PDF → Feature Extraction → ML Model → Prediction → API Response
```

---

## 📊 Model Performance

Evaluation performed using **Stratified 5-Fold Cross-Validation**.

### 🔹 Performance Comparison

| Model         | Accuracy   | Precision  | Recall     | F1 Score   | CV Mean F1 |
| ------------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Random Forest | 0.7989     | 0.7995     | 0.7989     | 0.7988     | 0.7963     |
| XGBoost       | 0.8061     | 0.8067     | 0.8061     | 0.8060     | **0.8107** |
| LightGBM      | **0.8137** | **0.8147** | **0.8137** | **0.8135** | 0.8075     |

### 🧠 Model Selection

XGBoost was selected for deployment based on:

* Highest **cross-validation F1 score**
* Better generalization capability
* Stable performance across folds

---

## 🚀 How to Run

### 1️⃣ Clone Repository

```bash
git clone https://github.com/amn2905/stegoai.git
cd stegoai
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Setup Environment

Create `.env` file:

```
MODEL_PATH=models/best_model.pkl
PORT=8000
MAX_FILE_SIZE_MB=10
```

---

### 4️⃣ Download Model

⚠️ Model is not included in this repository.

👉 Download from:

```
[PASTE-YOUR-GOOGLE-DRIVE-LINK-HERE(https://drive.google.com/file/d/1sLig5TaZXeAZyS_E7N3tpdcOxLiToyCE/view?usp=drive_link)
```

👉 Place file here:

```
models/best_model.pkl
```

---

### 5️⃣ Run API

```bash
uvicorn api.main:app --reload
```

---

### 6️⃣ Open API Docs

```
http://127.0.0.1:8000/docs
```

---

## 📡 API Endpoints

| Endpoint      | Method | Description              |
| ------------- | ------ | ------------------------ |
| `/`           | GET    | Health check             |
| `/predict`    | POST   | Feature-based prediction |
| `/upload-pdf` | POST   | Upload PDF file          |
| `/model-info` | GET    | Model information        |

---

## 📦 Example Response

```json
{
  "prediction": "Stego",
  "confidence": 0.82,
  "risk_level": "High"
}
```

---

## 🐳 Docker Usage

### Build Image

```bash
docker build -t stegoai .
```

### Run Container

```bash
docker run -p 8000:8000 stegoai
```

---

## 📁 Project Structure

```
api/        → FastAPI service layer
src/        → ML pipeline & feature engineering
models/     → trained models
results/    → metrics & logs
docs/       → documentation
demo/       → sample inputs/outputs
```

---

## 🧪 Dataset

* ~19K samples
* 8 steganography techniques
* Multiple payload variants

---

## 🛠️ Tech Stack

* Python
* Scikit-learn
* XGBoost
* LightGBM
* FastAPI
* Optuna

---

## 🔐 Security Focus

* Detects covert data patterns
* Identifies structural anomalies
* Designed for forensic applications

---

## 📈 Future Scope

* Image / Audio / Video steganalysis
* Deep learning models
* Real-time detection

---

## 🤝 Collaboration

For research, funding, or deployment:

📩 Email: [hamidamaan3@gmail.com](mailto:hamidamaan3@gmail.com)

---

## 📜 License

All Rights Reserved.

---

## 🧠 Final Note

StegoAI is a complete machine learning-based steganalysis system designed for real-world cybersecurity challenges.
