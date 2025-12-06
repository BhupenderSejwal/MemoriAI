# api_main.py – FastAPI entrypoint for MemoriAI API + MLOps

import os
import sys
from fastapi import FastAPI

# --- src klasörünü PYTHONPATH'e ekle ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # MemoriAI klasörü
SRC_DIR = os.path.join(BASE_DIR, "src")
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)
# ---------------------------------------

from config.logging_config import logger
from api import mlops_router
from routers import profile_router, reminder_router, dashboard_router


# ========================
# 1) FastAPI App nesnesini oluştur
# ========================
app = FastAPI(
    title="MemoriAI API",
    description="MLOps + Microservices for Assignment 6",
    version="1.0.0",
)

logger.info("[API] FastAPI MemoriAI app starting...")


# ========================
# 2) Router'ları dahil et
# ========================

# Eski servisler
app.include_router(profile_router.router)
app.include_router(reminder_router.router)
app.include_router(dashboard_router.router)

# Yeni MLOps servisleri
app.include_router(mlops_router.router)

logger.info("[API] Routers loaded successfully")


# ========================
# 3) Basit health/root endpoint
# ========================
@app.get("/")
def root():
    return {
        "message": "MemoriAI API is running. See /docs for API UI.",
        "endpoints": [
            "/profile/",
            "/reminder/",
            "/dashboard/",
            "/mlops/train",
            "/mlops/predict",
            "/mlops/health",
        ],
    }
