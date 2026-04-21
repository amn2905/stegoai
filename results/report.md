# 📊 StegoAI – Model Evaluation Report

## 📌 Overview

This report summarizes the performance of machine learning models developed for **PDF steganalysis detection**. The objective is to accurately classify files as **Clean** or **Stego (containing hidden data)** using engineered forensic features.

---

## 🧠 Models Evaluated

| Model         | Category           |
| ------------- | ------------------ |
| Random Forest | Ensemble (Bagging) |
| XGBoost       | Gradient Boosting  |
| LightGBM      | Gradient Boosting  |

---

## 📊 Performance Summary

| Model         | Accuracy   | Precision  | Recall     | F1 Score   | CV Mean    |
| ------------- | ---------- | ---------- | ---------- | ---------- | ---------- |
| Random Forest | 0.7989     | 0.7995     | 0.7989     | 0.7988     | 0.7963     |
| XGBoost       | 0.8061     | 0.8067     | 0.8061     | 0.8060     | **0.8107** |
| LightGBM      | **0.8137** | **0.8147** | **0.8137** | **0.8135** | 0.8075     |

---

## 🏆 Best Model

### 👉 XGBoost (Selected Model)

Although LightGBM shows slightly higher test metrics, **XGBoost is selected as the best model** due to:

* ✅ Higher cross-validation stability (CV Mean: 0.8107)
* ✅ Better generalization capability
* ✅ Robustness against overfitting
* ✅ Consistent performance across folds

---

## 🔍 Model-wise Analysis

### 🔹 Random Forest

* Baseline ensemble model
* Moderate performance
* Higher training time due to large number of trees
* Less effective in capturing complex feature interactions

---

### 🔹 XGBoost

* Strong generalization performance
* Balanced bias-variance tradeoff
* Performs well on structured and engineered features
* Selected for deployment

---

### 🔹 LightGBM

* Fastest training among all models
* Slightly higher test metrics
* Efficient for large-scale data
* Minor risk of overfitting compared to XGBoost

---

## 📈 Evaluation Metrics Explained

* **Accuracy** → Overall correctness
* **Precision** → False positive control
* **Recall** → Detection capability
* **F1 Score** → Balanced metric (primary metric used)
* **CV Mean** → Generalization performance

---

## 📊 Visual Results

Model performance is further supported by:

* Confusion Matrix
* ROC Curve (AUC ≈ 0.88+)
* Performance Comparison Graph

Available in:

```id="y7u1dp"
results/plots/
```

---

## 🧪 Feature Engineering Insights

The system leverages **15 engineered features** including:

* Metadata entropy
* Structural complexity score
* XREF gap analysis
* Padding byte ratio
* Text-to-nontext ratio

These features enable detection of:

* Hidden payload patterns
* Structural anomalies
* Covert communication indicators

---

## 🚀 Conclusion

* Gradient boosting models outperform bagging methods for this task
* XGBoost provides the best trade-off between performance and stability
* The system achieves **~81% F1-score**, demonstrating strong capability in detecting hidden data

---

## 🔮 Future Improvements

* Advanced byte-level analysis
* Deep learning-based steganalysis
* Multi-modal extension (Image, Audio, Video)
* Real-time large-scale deployment

---

## 🧠 Final Statement

StegoAI demonstrates a **practical and scalable approach** to detecting hidden data in documents, combining machine learning with forensic feature engineering for cybersecurity applications.

---
