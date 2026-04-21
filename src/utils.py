# ===================== IMPORTS =====================
import logging
import os
from logging.handlers import RotatingFileHandler
from config import PATH_CONFIG, APP_CONFIG

# ===================== LOGGER SETUP =====================
def setup_logger(name="stego_logger"):

    log_file = PATH_CONFIG["log_file"]
    log_level = APP_CONFIG.get("env", "development")

    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    logger = logging.getLogger(name)

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    # ===================== LOG LEVEL =====================
    level = logging.INFO if log_level == "production" else logging.DEBUG
    logger.setLevel(level)

    # ===================== FORMAT =====================
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # ===================== FILE HANDLER (ROTATION) =====================
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=5 * 1024 * 1024,   # 5MB
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    # ===================== CONSOLE HANDLER =====================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # ===================== ADD HANDLERS =====================
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger