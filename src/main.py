"""
File: main.py
Project: MemoriAI (Assignment 5 – DevOps Monitoring/Security & Secrets Management)
Developer: Nejla (Tessa) Ayvazoglu
Role: AI/ML Developer, Backend Integration
Date: 2025-11-28

Description:
This script runs the main FastAPI application for Use Case 1 – Cognitive & Identity Assistance.
It includes API routes for cognitive recall, word-aid generation, and profile memory logic.
Implements vector-based semantic search and LLM summarization features.

Updated for Assignment 5:
- Reads DB and ML experiment secrets from Docker environment variables (.env)
- Logs non-sensitive configuration details at startup for monitoring and auditing.
"""

from fastapi import FastAPI
from routers.reminder_router import router as reminder_router
from routers.dashboard_router import router as dashboard_router
from routers import profile_router

from config.logging_config import logger          # logging config
from config.config import Config                  # ✅ ENV + YAML based config

# Load configuration once at startup
cfg = Config()
logger.info("[CONFIG] Config object initialised from config.yml and environment variables")

app = FastAPI(
    title="MemoriAI Cognitive Service API",
    version="1.0",
    description="Cognitive Assist + Reminder + Dashboard Feed",
)

logger.info("[API] MemoriAI FastAPI app instance created")

# Attach config to app state (so routers can use it if needed)
app.state.config = cfg

# Routers
app.include_router(reminder_router)
app.include_router(dashboard_router)
app.include_router(profile_router.router)


@app.on_event("startup")
async def startup_event():
    logger.info("[API] FastAPI startup event triggered")

    # 🔐 Docker Secrets / ENV values in use (NO PASSWORD LOGGING)
    logger.info(
        "[SECRETS] DB config loaded: host=%s port=%s user=%s",
        cfg.db_host,
        cfg.db_port,
        cfg.db_username,
    )

    logger.info(
        "[SECRETS] ML experiment config: name=%s version=%s epochs=%d "
        "C=%.3f expected_acc=%.2f features=%s",
        cfg.experiment_name,
        cfg.experiment_version,
        cfg.num_epochs,
        cfg.hyperparam_c,
        cfg.expected_accuracy,
        ",".join(cfg.feature_names),
    )

    # İstersen ileride burada dummy bir training job da tetikleyebilirsin
    # örn: run_experiment(cfg)


@app.get("/")
def healthcheck():
    logger.info("[API] Healthcheck endpoint called")
    return {"status": "ok", "service": "MemoriAI Cognitive Service"}
