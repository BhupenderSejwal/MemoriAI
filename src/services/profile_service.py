# src/services/profile_service.py
from utils.sql_manager import SQLManager
from utils.user_manager import UserManager
from utils.config import Config
from config.logging_config import logger

class ProfileService:
    def __init__(self):
        cfg = Config()
        self.sql = SQLManager(cfg.db_path)
        self.um = UserManager(self.sql)
        logger.info("[PROFILE_SERVICE] Initialized for user_id=%s", self.um.user_id)

    def get_profile(self):
        logger.info("[PROFILE_SERVICE] get_profile called")
        return self.um.user_info

    def update_profile(self, data: dict):
        logger.info(
            "[PROFILE_SERVICE] update_profile called with keys=%s", list(data.keys())
        )
        return self.um.add_user_info_to_database(data)
