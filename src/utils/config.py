import os
from pathlib import Path
from yaml import load, Loader

class Config:
    def __init__(self):
        # 📂 Automatically detect the project root (src folder)
        SRC_DIR = Path(__file__).resolve().parents[1]
        CONFIG_PATH = SRC_DIR / "config" / "config.yml"

        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            config = load(f, Loader=Loader)

        # ========== YAML CONFIG (EXISTING) ==========
        # 🔹 Directories
        self.db_path = str((SRC_DIR / config["directories"]["db_path"]).resolve())
        self.vectordb_dir = str((SRC_DIR / config["directories"]["vectordb_dir"]).resolve())

        # 🔹 LLM Configuration
        self.chat_model = config["llm_config"]["chat_model"]
        self.summary_model = config["llm_config"]["summary_model"]
        self.rag_model = config["llm_config"]["rag_model"]
        self.temperature = config["llm_config"]["temperature"]

        # 🔹 Chat History Configuration
        self.max_history_pairs = config["chat_history_config"]["max_history_pairs"]
        self.max_characters = config["chat_history_config"]["max_characters"]
        self.max_tokens = config["chat_history_config"]["max_tokens"]

        # 🔹 Agent Configuration
        self.max_function_calls = config["agent_config"]["max_function_calls"]

        # 🔹 VectorDB Configuration
        self.collections = config["vectordb_config"]["collections"]
        self.embedding_model = config["vectordb_config"]["embedding_model"]
        self.k = config["vectordb_config"]["k"]

        # ============================================
        # 🔐 ENV SECRETS (NEW — REQUIRED FOR ASSIGNMENT 5)
        # ============================================

        # 📌 DB Secrets
        self.db_username = os.getenv("DB_USERNAME", "default_user")
        self.db_password = os.getenv("DB_PASSWORD", "default_pass")
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))

        # 📌 ML Experiment Secrets
        feature_names_string = os.getenv("FEATURE_NAMES", "")
        self.feature_names = [
            f.strip() for f in feature_names_string.split(",") if f.strip()
        ]

        self.hyperparam_c = float(os.getenv("HYPERPARAM_C", 1.0))
        self.expected_accuracy = float(os.getenv("EXPECTED_ACCURACY", 0.80))
        self.num_epochs = int(os.getenv("NUM_EPOCHS", 10))
        self.experiment_name = os.getenv("EXPERIMENT_NAME", "default_exp")
        self.experiment_version = os.getenv("EXPERIMENT_VERSION", "v1")
