# src/config/logging_config.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import os

# Project root = src/
SRC_DIR = Path(__file__).resolve().parent.parent

# logs directory = src/logs
LOG_DIR = SRC_DIR / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

logger = logging.getLogger("memori_ai")
logger.setLevel(logging.DEBUG)  # DEBUG dahil hepsini göster

if not logger.handlers:
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Log file handler
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=1_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)

    # Console handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

# Logların kök loggere gitmesini engelle
logger.propagate = False

# --- DB config loglama (env'den okuyup debug + info yaz) ---
db_user = os.getenv("DB_USERNAME")
db_host = os.getenv("DB_HOST")

logger.debug(f"DEBUG .env values: USER={db_user}, HOST={db_host}")
logger.info(f"[CONFIG] Loaded DB config for user={db_user}")
