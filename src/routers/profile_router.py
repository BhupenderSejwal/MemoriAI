from fastapi import APIRouter, HTTPException
from utils.sql_manager import SQLManager
from utils.user_manager import UserManager
from utils.config import Config
from config.logging_config import logger

router = APIRouter(prefix="/profile", tags=["Profile"])
cfg = Config()
sql = SQLManager(cfg.db_path)
um = UserManager(sql)

@router.get("/")
def get_profile():
    logger.info("[PROFILE] GET /profile/ called")
    return um.user_info

@router.post("/set")
def set_profile(data: dict):
    logger.info("[PROFILE] POST /profile/set called with keys=%s", list(data.keys()))
    try:
        state, msg = um.add_user_info_to_database(data)
        if not state.startswith("Function call successful"):
            logger.warning("[PROFILE] Profile update failed: %s", msg)
            raise ValueError(msg)

        um.refresh_user_info()
        logger.info("[PROFILE] Profile updated successfully for user_id=%s", um.user_id)
        return {"status": "ok", "profile": um.user_info}
    except Exception as e:
        logger.error("[PROFILE] Error updating profile: %s", str(e))
        raise HTTPException(status_code=400, detail=str(e))
