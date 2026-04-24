import sqlite3
import os
from datetime import datetime

DB_FILE = "app_history.db"

def init_db():
    """Initialize the DB and migrate schema if needed."""
    with sqlite3.connect(DB_FILE) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS activity_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                tool_endpoint TEXT NOT NULL,
                status_code INTEGER NOT NULL,
                user_agent TEXT
            )
        """)
        # Migrate: add new columns if they don't exist
        existing = {row[1] for row in conn.execute("PRAGMA table_info(activity_logs)").fetchall()}
        if "tool_name" not in existing:
            conn.execute("ALTER TABLE activity_logs ADD COLUMN tool_name TEXT DEFAULT ''")
        if "category" not in existing:
            conn.execute("ALTER TABLE activity_logs ADD COLUMN category TEXT DEFAULT ''")
        if "detail" not in existing:
            conn.execute("ALTER TABLE activity_logs ADD COLUMN detail TEXT DEFAULT ''")
        if "duration_ms" not in existing:
            conn.execute("ALTER TABLE activity_logs ADD COLUMN duration_ms INTEGER DEFAULT 0")
        conn.commit()


def log_activity(tool_endpoint, status_code, user_agent="",
                 tool_name="", category="", detail="", duration_ms=0):
    """Log a tool usage event with rich metadata."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn.execute(
                """INSERT INTO activity_logs
                   (timestamp, tool_endpoint, status_code, user_agent,
                    tool_name, category, detail, duration_ms)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (current_time, tool_endpoint, status_code,
                 str(user_agent)[:100], tool_name[:100],
                 category[:50], str(detail)[:300], int(duration_ms))
            )
            conn.commit()
    except Exception as e:
        print(f"[Logger] Failed to log activity: {e}")


def get_logs(limit=200):
    """Retrieve recent activity logs with all metadata."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                """SELECT id, timestamp, tool_endpoint, status_code, user_agent,
                          tool_name, category, detail, duration_ms
                   FROM activity_logs ORDER BY id DESC LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            return [
                {
                    "id": row["id"],
                    "timestamp": row["timestamp"],
                    "tool_endpoint": row["tool_endpoint"],
                    "status_code": row["status_code"],
                    "user_agent": row["user_agent"] or "",
                    "tool_name": row["tool_name"] or row["tool_endpoint"],
                    "category": row["category"] or "",
                    "detail": row["detail"] or "",
                    "duration_ms": row["duration_ms"] or 0,
                }
                for row in rows
            ]
    except Exception as e:
        print(f"[Logger] Failed to fetch logs: {e}")
        return []


def get_stats():
    """Get summary statistics for the dashboard header."""
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.row_factory = sqlite3.Row
            total = conn.execute("SELECT COUNT(*) as c FROM activity_logs").fetchone()["c"]
            success = conn.execute("SELECT COUNT(*) as c FROM activity_logs WHERE status_code >= 200 AND status_code < 300").fetchone()["c"]
            failed = conn.execute("SELECT COUNT(*) as c FROM activity_logs WHERE status_code >= 400").fetchone()["c"]
            # Most used tool
            top_tool = conn.execute(
                """SELECT tool_name, COUNT(*) as cnt FROM activity_logs
                   WHERE tool_name != '' GROUP BY tool_name ORDER BY cnt DESC LIMIT 1"""
            ).fetchone()
            # Today's count
            today = datetime.now().strftime("%Y-%m-%d")
            today_count = conn.execute(
                "SELECT COUNT(*) as c FROM activity_logs WHERE timestamp LIKE ?",
                (f"{today}%",)
            ).fetchone()["c"]
            return {
                "total": total,
                "success": success,
                "failed": failed,
                "top_tool": top_tool["tool_name"] if top_tool else "-",
                "top_tool_count": top_tool["cnt"] if top_tool else 0,
                "today": today_count,
            }
    except Exception as e:
        print(f"[Logger] Failed to get stats: {e}")
        return {"total": 0, "success": 0, "failed": 0, "top_tool": "-", "top_tool_count": 0, "today": 0}


def clear_logs():
    try:
        with sqlite3.connect(DB_FILE) as conn:
            conn.execute("DELETE FROM activity_logs")
            conn.commit()
    except Exception as e:
        print(f"[Logger] Failed to clear logs: {e}")
