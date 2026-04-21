# ===================== IMPORTS =====================
import os
from dotenv import load_dotenv

# ===================== LOAD ENV =====================
load_dotenv()

# ===================== GENERAL =====================
APP_CONFIG = {
    "name": os.getenv("APP_NAME", "StegoAI"),
    "env": os.getenv("APP_ENV", "development"),
    "version": os.getenv("APP_VERSION", "1.0")
}

# ===================== PATHS =====================
PATH_CONFIG = {
    "data_path": os.getenv("DATA_PATH", "dataset/"),
    "model_path": os.getenv("MODEL_PATH", "models/best_model.pkl"),
    "log_file": os.getenv("LOG_FILE", "logs/api.log")
}

# ===================== TRAINING =====================
TRAINING_CONFIG = {
    "test_size": float(os.getenv("TEST_SIZE", 0.2)),
    "random_state": int(os.getenv("RANDOM_STATE", 42)),
    "pca_components": int(os.getenv("PCA_COMPONENTS", 3))
}

# ===================== MODEL CONFIG =====================
MODEL_CONFIG = {

    "rf": {
        "n_estimators": int(os.getenv("RF_N_ESTIMATORS", 100)),
        "max_depth": int(os.getenv("RF_MAX_DEPTH", 20))
    },

    "xgb": {
        "n_estimators": int(os.getenv("XGB_N_ESTIMATORS", 100)),
        "max_depth": int(os.getenv("XGB_MAX_DEPTH", 6)),
        "learning_rate": float(os.getenv("XGB_LR", 0.1))
    },

    "lgbm": {
        "n_estimators": int(os.getenv("LGBM_N_ESTIMATORS", 100)),
        "max_depth": int(os.getenv("LGBM_MAX_DEPTH", -1)),
        "learning_rate": float(os.getenv("LGBM_LR", 0.1))
    }
}

# ===================== FEATURE CONFIG =====================
FEATURE_CONFIG = {
    "feature_count": int(os.getenv("FEATURE_COUNT", 15))
}

# ===================== API CONFIG =====================
API_CONFIG = {
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", 8000)),
    "max_file_size_mb": int(os.getenv("MAX_FILE_SIZE_MB", 10))
}