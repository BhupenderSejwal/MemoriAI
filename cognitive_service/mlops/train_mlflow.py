# cognitive_service/mlops/train_mlflow.py

import os
from pathlib import Path

import mlflow
import mlflow.sklearn
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

# --- Logging ---
try:
    from src.config.logging_config import logger
except Exception:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

# --- Baz dizinler (MemoriAI root) ---
# Bu dosya: MemoriAI/cognitive_service/mlops/train_mlflow.py
BASE_DIR = Path(__file__).resolve().parents[2]   # -> MemoriAI/
DEFAULT_DATA_PATH = BASE_DIR / "src" / "data" / "memoriai_train.csv"
DEFAULT_MODEL_DIR = BASE_DIR / "models"


def train_memoriai_model(
    data_path: str | None = None,
    model_dir: str | None = None,
) -> dict:
    """
    Simple text classification training pipeline for MemoriAI.
    Logs params/metrics/model to MLflow and saves a local pickle model.
    """

    data_path = Path(data_path) if data_path else DEFAULT_DATA_PATH
    model_dir_path = Path(model_dir) if model_dir else DEFAULT_MODEL_DIR

    logger.info("[MLOPS] MemoriAI training pipeline started")
    logger.info("[MLOPS] Using data file: %s", data_path)
    logger.info("[MLOPS] Model dir: %s", model_dir_path)

    if not data_path.exists():
        logger.error("[MLOPS] Training data not found at %s", data_path)
        raise FileNotFoundError(f"Training data not found at {data_path}")

    df = pd.read_csv(data_path)

    if "text" not in df.columns or "label" not in df.columns:
        raise ValueError("Training CSV must contain 'text' and 'label' columns.")

    X = df["text"].astype(str)
    y = df["label"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    params = {
        "C": 1.0,
        "max_iter": 1000,
        "solver": "lbfgs",
    }

    # MLflow experiment
    mlflow.set_experiment("MemoriAI_Text_Classification")

    with mlflow.start_run() as run:
        run_id = run.info.run_id
        logger.info("[MLOPS] MLflow run started: %s", run_id)

        # hyperparams
        mlflow.log_params(params)

        # pipeline: TF-IDF + Logistic Regression
        pipeline = Pipeline(
            [
                ("tfidf", TfidfVectorizer()),
                ("clf", LogisticRegression(**params)),
            ]
        )

        pipeline.fit(X_train, y_train)

        # metrics
        y_pred = pipeline.predict(X_test)
        acc = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average="weighted")

        mlflow.log_metric("accuracy", acc)
        mlflow.log_metric("f1_score", f1)

        logger.info(
            "[MLOPS] Training completed: accuracy=%.4f, f1_score=%.4f",
            acc,
            f1,
        )

        # log model to MLflow
        model_info = mlflow.sklearn.log_model(
            sk_model=pipeline,
            artifact_path="memoriai_model",
            registered_model_name="MemoriAI_Text_Model",
        )

        # save local model for inference endpoint
        model_dir_path.mkdir(parents=True, exist_ok=True)
        local_model_path = model_dir_path / "memoriai_latest.pkl"

        import joblib
        joblib.dump(pipeline, local_model_path)
        logger.info("[MLOPS] Local model saved to %s", local_model_path.resolve())

        mlflow.set_tag("use_case", "memoriai_text_classification")

    logger.info("[MLOPS] MemoriAI training pipeline finished")

    return {
        "run_id": run_id,
        "accuracy": acc,
        "f1_score": f1,
        "mlflow_model_uri": model_info.model_uri,
        "local_model_path": str(local_model_path),
    }
