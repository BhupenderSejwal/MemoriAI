# src/services/reminder_service.py
from typing import List, Optional, Tuple
from datetime import datetime, timezone
from utils.sql_manager import SQLManager

# Logging import
from config.logging_config import logger


def now_iso() -> str:
    """
    Returns the current UTC time in ISO 8601 format.
    Example: 2025-11-16T18:45:23Z
    """
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class ReminderService:
    """
    Service layer for CRUD operations on reminders.

    This class is responsible for:
    - Creating reminders
    - Listing reminders with optional status filtering
    - Updating reminder status (pending/done/canceled)
    - Counting reminders per status

    Logging (Assignment 4 – DevOps Log Management):
    - Logs service initialization
    - Logs reminder creation
    - Logs listing operations
    - Logs status updates
    - Logs statistics calculation
    """

    def __init__(self, sql: SQLManager, user_id: int):
        self.sql = sql
        self.user_id = user_id
        if hasattr(self.sql, "ensure_reminders_table"):
            self.sql.ensure_reminders_table()

        # INFO log: service initialized
        logger.info(
            "ReminderService initialized for user_id=%s", self.user_id
        )

    def create(self, title: str, due_at: Optional[str]) -> int:
        """
        Create a new reminder for the current user.
        """
        created = now_iso()
        updated = created

        logger.info(
            "Creating reminder: user_id=%s, title='%s', due_at=%s",
            self.user_id, title, due_at
        )

        cur = self.sql.conn.execute(
            """
            INSERT INTO reminders(user_id, title, due_at, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (self.user_id, title, due_at, "pending", created, updated)
        )
        self.sql.conn.commit()
        reminder_id = cur.lastrowid

        logger.info(
            "Reminder created successfully: id=%s, user_id=%s",
            reminder_id, self.user_id
        )
        return reminder_id

    def list(
        self,
        status: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Tuple[List[dict], int]:
        """
        List reminders for the current user, optionally filtered by status.
        Supports pagination via limit and offset.
        """
        logger.info(
            "Listing reminders: user_id=%s, status=%s, limit=%s, offset=%s",
            self.user_id, status, limit, offset
        )

        params = [self.user_id]
        where = "WHERE user_id = ?"
        if status:
            where += " AND status = ?"
            params.append(status)

        count_row = self.sql.conn.execute(
            f"SELECT COUNT(*) FROM reminders {where}", params
        ).fetchone()
        total = count_row[0] if count_row else 0

        params += [limit, offset]
        rows = self.sql.conn.execute(
            f"""
            SELECT id, user_id, title, due_at, status, created_at, updated_at
            FROM reminders
            {where}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
            """,
            params
        ).fetchall()

        items = [
            dict(
                zip(
                    ["id", "user_id", "title", "due_at", "status", "created_at", "updated_at"],
                    r
                )
            ) for r in rows
        ]

        logger.info(
            "Listed reminders: user_id=%s, status=%s, returned=%s, total=%s",
            self.user_id, status, len(items), total
        )
        return items, total

    def update_status(self, reminder_id: int, status: str) -> bool:
        """
        Update the status of a reminder (pending/done/canceled).
        """
        updated = now_iso()
        logger.info(
            "Updating reminder status: id=%s, user_id=%s, new_status=%s",
            reminder_id, self.user_id, status
        )

        res = self.sql.conn.execute(
            """
            UPDATE reminders
            SET status=?, updated_at=?
            WHERE id=? AND user_id=?
            """,
            (status, updated, reminder_id, self.user_id)
        )
        self.sql.conn.commit()
        success = res.rowcount > 0

        if success:
            logger.info(
                "Reminder status updated successfully: id=%s, user_id=%s, new_status=%s",
                reminder_id, self.user_id, status
            )
        else:
            logger.warning(
                "Reminder status update failed: id=%s, user_id=%s, new_status=%s",
                reminder_id, self.user_id, status
            )
        return success

    def count_by_status(self) -> dict:
        """
        Count reminders by status for the current user.
        Returns a dict: {pending, done, canceled, total}
        """
        logger.info(
            "Calculating reminder statistics by status for user_id=%s",
            self.user_id
        )

        stats = {}
        for s in ["pending", "done", "canceled"]:
            row = self.sql.conn.execute(
                "SELECT COUNT(*) FROM reminders WHERE user_id=? AND status=?",
                (self.user_id, s)
            ).fetchone()
            stats[s] = row[0] if row else 0

        total_row = self.sql.conn.execute(
            "SELECT COUNT(*) FROM reminders WHERE user_id=?",
            (self.user_id,)
        ).fetchone()
        stats["total"] = total_row[0] if total_row else 0

        logger.info(
            "Reminder statistics computed for user_id=%s: %s",
            self.user_id, stats
        )
        return stats
