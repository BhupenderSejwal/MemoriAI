# cognitive_service/mlops/inference.py

from pathlib import Path
from typing import List

try:
    from src.config.logging_config import logger
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

import joblib

BASE_DIR = Path(__file__).resolve().parents[2]  # MemoriAI/
DEFAULT_MODEL_PATH = BASE_DIR / "models" / "memoriai_latest.pkl"


def load_latest_model(model_path: str | None = None):
    """
    Load the latest local model trained by train_memoriai_model.
    """
    path = Path(model_path) if model_path else DEFAULT_MODEL_PATH
    if not path.exists():
        logger.error("[MLOPS] Model file not found at %s", path)
        raise FileNotFoundError(f"Model file not found at {path}")

    logger.info("[MLOPS] Loading model from %s", path.resolve())
    return joblib.load(path)


def predict_texts(model, texts: List[str]) -> List[str]:
    """
    Run predictions on a list of input texts.
    """
    logger.info("[MLOPS] Predict called for %d texts", len(texts))
    preds = model.predict(texts)
    return preds.tolist()
