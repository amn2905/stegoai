# ===================== IMPORTS =====================
import os
import json
import joblib
import numpy as np

from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier

from config import TRAINING_CONFIG, MODEL_CONFIG, PATH_CONFIG
from src.data_loader import load_dataset
from src.utils import setup_logger

logger = setup_logger("ml_pipeline")


# ===================== PIPELINE =====================
class StegPipeline:

    def __init__(self):
        # Configs
        self.data_path = PATH_CONFIG["data_path"]
        self.model_path = PATH_CONFIG["model_path"]

        self.test_size = TRAINING_CONFIG["test_size"]
        self.random_state = TRAINING_CONFIG["random_state"]
        self.pca_components = TRAINING_CONFIG["pca_components"]

        # Preprocessing
        self.scaler = StandardScaler()
        self.pca = PCA(n_components=self.pca_components)

        # Models
        self.models = {
            "RandomForest": RandomForestClassifier(**MODEL_CONFIG["rf"]),
            "XGBoost": XGBClassifier(
                use_label_encoder=False,
                eval_metric="logloss",
                **MODEL_CONFIG["xgb"]
            ),
            "LightGBM": LGBMClassifier(**MODEL_CONFIG["lgbm"])
        }

        self.best_model = None
        self.best_name = None

    # ===================== TRAIN =====================
    def train(self):
        logger.info("Training started...")

        # Load dataset
        X, y = load_dataset(self.data_path)

        # Preprocessing
        X = self.scaler.fit_transform(X)
        X = self.pca.fit_transform(X)

        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=self.test_size,
            random_state=self.random_state,
            stratify=y
        )

        results = {}
        best_f1 = 0

        # Train each model
        for name, model in self.models.items():
            logger.info(f"Training {name}")

            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            model.fit(X_train, y_train)

            preds = model.predict(X_test)

            acc = accuracy_score(y_test, preds)
            prec = precision_score(y_test, preds, zero_division=0)
            rec = recall_score(y_test, preds, zero_division=0)
            f1 = f1_score(y_test, preds, zero_division=0)

            results[name] = {
                "accuracy": round(acc, 4),
                "precision": round(prec, 4),
                "recall": round(rec, 4),
                "f1_score": round(f1, 4),
                "cv_mean": round(float(np.mean(cv_scores)), 4)
            }

            logger.info(
                f"{name} → Acc:{acc:.4f} | Prec:{prec:.4f} | Rec:{rec:.4f} | F1:{f1:.4f}"
            )

            # Select best based on F1
            if f1 > best_f1:
                best_f1 = f1
                self.best_model = model
                self.best_name = name

        logger.info(f"Best Model: {self.best_name}")

        # ===================== SAVE =====================
        os.makedirs("models", exist_ok=True)
        os.makedirs("results", exist_ok=True)

        # Save best model
        joblib.dump(self.best_model, self.model_path)

        # Save metrics
        with open("results/metrics.json", "w") as f:
            json.dump(results, f, indent=4)

        # Save metadata
        metadata = {
            "best_model": self.best_name,
            "metric": "f1_score"
        }

        with open("models/model_metadata.json", "w") as f:
            json.dump(metadata, f, indent=4)

        logger.info("Training completed successfully")

        return results

    # ===================== LOAD MODEL =====================
    def load_model(self):
        if not os.path.exists(self.model_path):
            raise FileNotFoundError("Model not found. Train first.")

        self.best_model = joblib.load(self.model_path)
        logger.info("Model loaded for inference")

    # ===================== PREDICT =====================
    def predict(self, features):
        if self.best_model is None:
            self.load_model()

        features = self.scaler.transform([features])
        features = self.pca.transform(features)

        pred = self.best_model.predict(features)[0]

        return "STEGO" if pred == 1 else "CLEAN"