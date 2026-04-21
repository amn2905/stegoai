# ===================== IMPORTS =====================
import os
import json
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from src.utils import setup_logger

logger = setup_logger("evaluation")


# ===================== EVALUATION =====================
def evaluate_model(model, X_test, y_test, save_dir="results"):

    logger.info("Evaluation started...")

    os.makedirs(save_dir, exist_ok=True)
    os.makedirs(os.path.join(save_dir, "plots"), exist_ok=True)

    # ===================== PREDICTIONS =====================
    preds = model.predict(X_test)

    # ===================== METRICS =====================
    acc = accuracy_score(y_test, preds)
    prec = precision_score(y_test, preds, zero_division=0)
    rec = recall_score(y_test, preds, zero_division=0)
    f1 = f1_score(y_test, preds, zero_division=0)

    report = classification_report(y_test, preds, output_dict=True)
    matrix = confusion_matrix(y_test, preds)

    # ===================== LOG =====================
    logger.info(f"Accuracy: {acc:.4f}")
    logger.info(f"Precision: {prec:.4f}")
    logger.info(f"Recall: {rec:.4f}")
    logger.info(f"F1 Score: {f1:.4f}")

    logger.info("Classification Report generated")
    logger.info(f"Confusion Matrix:\n{matrix}")

    # ===================== SAVE METRICS =====================
    metrics = {
        "accuracy": round(acc, 4),
        "precision": round(prec, 4),
        "recall": round(rec, 4),
        "f1_score": round(f1, 4),
        "classification_report": report
    }

    with open(os.path.join(save_dir, "evaluation.json"), "w") as f:
        json.dump(metrics, f, indent=4)

    # ===================== CONFUSION MATRIX PLOT =====================
    plt.figure(figsize=(5, 4))
    sns.heatmap(matrix, annot=True, fmt="d", cmap="Blues")
    plt.xlabel("Predicted")
    plt.ylabel("Actual")
    plt.title("Confusion Matrix")

    cm_path = os.path.join(save_dir, "plots", "confusion_matrix.png")
    plt.savefig(cm_path)
    plt.close()

    logger.info(f"Confusion matrix saved: {cm_path}")

    # ===================== RETURN =====================
    return metrics