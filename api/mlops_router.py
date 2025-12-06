# api/mlops_router.py
import logging
from fastapi import APIRouter
from cognitive_service.mlops.train_mlflow import train_memoriai_model
from cognitive_service.mlops.inference import load_latest_model, predict_texts

router = APIRouter(prefix="/mlops", tags=["MLOps"])

@router.post("/train")
def train_pipeline():
    logging.info("[API] /mlops/train called")
    result = train_memoriai_model()
    return {"status": "ok", "details": result}
 
@router.post("/predict")
def predict_endpoint(payload: dict):
    """
    Example payload:
    {
      "texts": [
        "What are my daughters' names?",
        "Where did I work in the past?"
      ]
    }
    """
    logging.info("[API] /mlops/predict called")
    model = load_latest_model()
    answers = predict_texts(model, payload["texts"])
    return {"answers": answers}

#@router.post("/predict")
#def predict_endpoint(payload: dict):
#    """
#    payload = {"texts": ["Hello, I forgot my pills", "I am fine today"]}
#    """
#    logging.info("[API] /mlops/predict called")
#    model = load_latest_model()
#    preds = predict_texts(model, payload["texts"])
#    return {"predictions": list(map(str, preds))}

@router.get("/health")
def health_check():
    logging.info("[API] /mlops/health called")
    return {"status": "running", "service": "MemoriAI MLOps"}
