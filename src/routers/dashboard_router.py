from fastapi import APIRouter
from utils.sql_manager import SQLManager
from utils.user_manager import UserManager
from services.reminder_service import ReminderService
from utils.config import Config
from config.logging_config import logger

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

def _deps():
    cfg = Config()
    sql = SQLManager(cfg.db_path)
    user = UserManager(sql)
    return sql, user

@router.get("/summary")
def dashboard_summary():
    sql, user = _deps()
    logger.info("[DASHBOARD] GET /dashboard/summary called for user_id=%s", user.user_id)

    reminder_svc = ReminderService(sql, user.user_id)
    reminder_stats = reminder_svc.count_by_status()

    chat_count = 0
    if hasattr(sql, "conn"):
        try:
            row = sql.conn.execute(
                "SELECT COUNT(*) FROM chat_history WHERE user_id=?", (user.user_id,)
            ).fetchone()
            chat_count = row[0] if row else 0
        except Exception as e:
            logger.error("[DASHBOARD] Error counting chat messages: %s", str(e))
            chat_count = 0

    logger.info(
        "[DASHBOARD] Summary built (reminders_total=%d, chat_count=%d)",
        reminder_stats.get("total", 0),
        chat_count,
    )

    return {
        "user_id": user.user_id,
        "reminders": reminder_stats,
        "chat_messages_total": chat_count,
        "notes": "Extend with more KPIs (e.g., latency, uptime, hallucination rate).",
    }
