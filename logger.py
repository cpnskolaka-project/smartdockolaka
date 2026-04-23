import sqlite3
import os
from datetime import datetime

DB_FILE = "app_history.db"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS activity_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            tool_endpoint TEXT NOT NULL,
            status_code INTEGER NOT NULL,
            user_agent TEXT
        )
    """)
    conn.commit()
    conn.close()

def log_activity(tool_endpoint, status_code, user_agent=""):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO activity_logs (timestamp, tool_endpoint, status_code, user_agent) VALUES (?, ?, ?, ?)",
            (current_time, tool_endpoint, status_code, str(user_agent)[:100])
        )
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to log activity: {e}")

def get_logs(limit=100):
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("SELECT id, timestamp, tool_endpoint, status_code, user_agent FROM activity_logs ORDER BY id DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        conn.close()
        
        logs = []
        for row in rows:
            logs.append({
                "id": row[0],
                "timestamp": row[1],
                "tool_endpoint": row[2],
                "status_code": row[3],
                "user_agent": row[4]
            })
        return logs
    except Exception as e:
        print(f"Failed to fetch logs: {e}")
        return []

def clear_logs():
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM activity_logs")
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Failed to clear logs: {e}")
