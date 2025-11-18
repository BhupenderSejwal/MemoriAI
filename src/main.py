"""
File: main.py
Project: MemoriAI (Assignment 3 – API Service Designs & Architecture)
Developer: Nejla (Tessa) Ayvazoglu
Role: AI/ML Developer, Backend Integration
Date: 2025-10-26

Description:
This script runs the main FastAPI application for Use Case 1 – Cognitive & Identity Assistance.
It includes API routes for cognitive recall, word-aid generation, and profile memory logic.
Implements vector-based semantic search and LLM summarization features.

Version: 1.1  (updated for Assignment 4 logging)
"""

# src/main.py
from fastapi import FastAPI
from routers.reminder_router import router as reminder_router
from routers.dashboard_router import router as dashboard_router
from routers import profile_router

from config.logging_config import logger  # logging config

app = FastAPI(
    title="MemoriAI Cognitive Service API",
    version="1.0",
    description="Cognitive Assist + Reminder + Dashboard Feed",
)

logger.info("[API] MemoriAI FastAPI app instance created")

# Routers
app.include_router(reminder_router)
app.include_router(dashboard_router)
app.include_router(profile_router.router)

@app.on_event("startup")
async def startup_event():
    logger.info("[API] FastAPI startup event triggered")

@app.get("/")
def healthcheck():
    logger.info("[API] Healthcheck endpoint called")
    return {"status": "ok", "service": "MemoriAI Cognitive Service"}
