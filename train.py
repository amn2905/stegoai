# ===================== IMPORTS =====================
from src.ml_pipeline import StegPipeline
from config import PATH_CONFIG
from src.utils import setup_logger

logger = setup_logger("train")


# ===================== MAIN =====================
def main():
    try:
        logger.info("Training process started")

        # Initialize pipeline
        pipeline = StegPipeline()

        # Train models
        results = pipeline.train()

        print("\n===== TRAINING RESULTS =====")
        for model, metrics in results.items():
            print(f"{model}: {metrics}")

        print("\n===== BEST MODEL =====")
        print(f"Model: {pipeline.best_name}")

        logger.info(f"Best Model: {pipeline.best_name}")

        # ===================== TEST INFERENCE =====================
        print("\n===== TEST INFERENCE =====")

        # Example feature input (dummy)
        sample_features = [
            120000, 45, 3.5, 200, 4.2,
            0.02, 0.5, 0.01, 0.3, 0.05,
            2, 0.8, 0.1, 0.7, 0.6
        ]

        prediction = pipeline.predict(sample_features)

        print(f"Sample Prediction: {prediction}")

        logger.info(f"Sample Prediction: {prediction}")

    except Exception as e:
        logger.error(f"Training failed: {e}")
        print(f"Error: {e}")


# ===================== ENTRY =====================
if __name__ == "__main__":
    main()