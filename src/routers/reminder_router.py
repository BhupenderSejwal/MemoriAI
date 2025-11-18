from fastapi import APIRouter, Depends, Query, HTTPException
from typing import Optional
from utils.sql_manager import SQLManager
from utils.user_manager import UserManager
from services.reminder_service import ReminderService
from schemas import ReminderCreate, ReminderListResponse, ReminderItem
from config.logging_config import logger

router = APIRouter(prefix="/reminder", tags=["reminder"])

def get_service() -> ReminderService:
    from utils.config import Config
    cfg = Config()
    sql = SQLManager(cfg.db_path)
    if hasattr(sql, "ensure_reminders_table"):
        sql.ensure_reminders_table()
    user = UserManager(sql)
    logger.info("[REMINDER] Service created for user_id=%s", user.user_id)
    return ReminderService(sql, user.user_id)

@router.post("/set", response_model=ReminderItem)
def set_reminder(payload: ReminderCreate, svc: ReminderService = Depends(get_service)):
    logger.info("[REMINDER] POST /reminder/set called (title=%s)", payload.title)
    rid = svc.create(payload.title, payload.due_at)
    items, _ = svc.list(limit=1, offset=0)
    created = next((i for i in items if i["id"] == rid), None)
    if not created:
        logger.error("[REMINDER] Creation failed for id=%s", rid)
        raise HTTPException(status_code=500, detail="Reminder creation failed.")
    logger.info("[REMINDER] Reminder created with id=%s", rid)
    return ReminderItem(**created)

@router.get("/list", response_model=ReminderListResponse)
def list_reminders(
    status: Optional[str] = Query(None, regex="^(pending|done|canceled)$"),
    limit: int = Query(50, ge=1, le=200),
    offset: int = Query(0, ge=0),
    svc: ReminderService = Depends(get_service),
):
    logger.info(
        "[REMINDER] GET /reminder/list called (status=%s, limit=%d, offset=%d)",
        status, limit, offset
    )
    items, total = svc.list(status=status, limit=limit, offset=offset)
    return ReminderListResponse(items=[ReminderItem(**i) for i in items], total=total)

@router.post("/delete")
def delete_reminder(reminder_id: int, svc: ReminderService = Depends(get_service)):
    logger.info("[REMINDER] POST /reminder/delete called (id=%d)", reminder_id)
    ok = svc.update_status(reminder_id, "canceled")
    if not ok:
        logger.warning("[REMINDER] delete_reminder: id=%d not found", reminder_id)
        raise HTTPException(status_code=404, detail="Reminder not found.")
    return {"ok": True, "reminder_id": reminder_id, "status": "canceled"}

@router.post("/mark-done")
def mark_done(reminder_id: int, svc: ReminderService = Depends(get_service)):
    logger.info("[REMINDER] POST /reminder/mark-done called (id=%d)", reminder_id)
    ok = svc.update_status(reminder_id, "done")
    if not ok:
        logger.warning("[REMINDER] mark_done: id=%d not found", reminder_id)
        raise HTTPException(status_code=404, detail="Reminder not found.")
    return {"ok": True, "reminder_id": reminder_id, "status": "done"}
