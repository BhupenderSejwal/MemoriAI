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

# Model dosyası
BASE_MODEL_PATH = Path(__file__).resolve().parents[2] / "models" / "memoriai_latest.pkl"

# LABEL → KİŞİSEL CEVAP HARİTASI
ANSWER_MAP = {
    "employment": (
        "You have more than 17 years of experience in banking and financial systems, "
        "working with COBOL, JCL, DB2, VSAM and mainframe batch processing. "
        "You worked many years at Akbank and also at TD Bank in Canada."
    ),
    "family": (
        "You have two daughters. Your older daughter is Mel (born in 2009) and "
        "your younger daughter is Lian (born in 2016). "
        "You live together as a family in Canada."
    ),
    "health": (
        "You sometimes experience stress, migraines and sleep issues, and you monitor "
        "things like vitamin D and skin conditions with your doctor."
    ),
    "study_ml": (
        "You studied Applied Artificial Intelligence and Machine Learning at Conestoga College "
        "and you work on projects like MemoriAI, SafePlayAI, VirexAI, credit risk models and "
        "toxicity detection APIs."
    ),
    "study_cyber": (
        "You are currently studying cybersecurity at Lambton College, including modules like "
        "operating system security, mobile application security, Linux, firewalls, VPNs and forensics."
    ),
    "future_goal": (
        "Your future goals include launching your AI startup, improving MemoriAI as a real assistant "
        "for memory and dementia support, and completing your cybersecurity diploma."
    ),
    "journal": (
        "This sounds like a personal reflection or journal-style note about your day and feelings. "
        "MemoriAI can store this as part of your personal timeline."
    ),
    "personal_interest": (
        "This is related to your personal interests and daily life, such as spending time with your "
        "family, cooking, or reading books like The Lord of the Rings."
    ),
    # Diğer label'lar için fallback hazır
}


def load_latest_model(model_path: str | None = None):
    """
    Load the latest local model trained by train_memoriai_model.
    """
    path = Path(model_path) if model_path else BASE_MODEL_PATH
    if not path.exists():
        logger.error("[MLOPS] Model file not found at %s", path)
        raise FileNotFoundError(f"Model file not found at {path}")

    logger.info("[MLOPS] Loading model from %s", path.resolve())
    return joblib.load(path)


def predict_texts(model, texts: List[str]) -> List[str]:
    """
    Run predictions on a list of input texts and return NATURAL LANGUAGE answers,
    not raw labels. The classifier is used internally.
    """
    logger.info("[MLOPS] Predict called for %d texts", len(texts))
    labels = model.predict(texts)

    answers: List[str] = []
    for label in labels:
        label_str = str(label)
        if label_str in ANSWER_MAP:
            answers.append(ANSWER_MAP[label_str])
        else:
            # Fallback cevabı – label'ı göstermeden genel bir cevap
            answers.append(
                f"This question seems related to your {label_str} memories. "
                "MemoriAI can use this to organize and recall your personal information."
            )

    return answers
