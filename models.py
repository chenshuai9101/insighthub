"""InsightHub 数据模型 - SQLite"""

import sqlite3
import os
import json
from datetime import datetime, timedelta
from config import DATABASE_URL

# 确保数据目录存在
os.makedirs(os.path.dirname(DATABASE_URL), exist_ok=True)


def get_db():
    """获取数据库连接"""
    conn = sqlite3.connect(DATABASE_URL)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db():
    """初始化数据库表"""
    conn = get_db()
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            api_key TEXT UNIQUE,
            plan TEXT DEFAULT 'free',
            analysis_count INTEGER DEFAULT 0,
            analysis_limit INTEGER DEFAULT 5,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS analysis_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            source_id TEXT NOT NULL,
            url TEXT,
            keyword TEXT,
            dimensions TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            result_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            completed_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            task_id INTEGER NOT NULL,
            interval_hours INTEGER DEFAULT 24,
            next_run TIMESTAMP,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (task_id) REFERENCES analysis_tasks(id)
        );

        CREATE TABLE IF NOT EXISTS subscriptions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            source_id TEXT NOT NULL,
            active INTEGER DEFAULT 1,
            expires_at TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        -- 创建一个匿名用户（免登录模式）
        INSERT OR IGNORE INTO users (id, email, api_key, plan, analysis_count, analysis_limit)
        VALUES (1, 'anonymous@insighthub.local', 'anon-00000000-0000-0000-0000-000000000000', 'free', 0, 5);
    """)

    conn.commit()
    conn.close()


# ---------- User Operations ----------

def get_or_create_user(email):
    """获取或创建用户"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user:
        conn.close()
        return dict(user)

    import uuid
    api_key = str(uuid.uuid4())
    cursor.execute(
        "INSERT INTO users (email, api_key) VALUES (?, ?)",
        (email, api_key),
    )
    conn.commit()
    user_id = cursor.lastrowid
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user)


def get_user_by_id(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def get_user_by_api_key(api_key):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE api_key = ?", (api_key,))
    user = cursor.fetchone()
    conn.close()
    return dict(user) if user else None


def increment_analysis_count(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET analysis_count = analysis_count + 1, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
        (user_id,),
    )
    conn.commit()
    conn.close()


def can_analyze(user_id):
    """检查用户是否还有分析次数"""
    if user_id == 1:
        return True  # 匿名用户不限制
    user = get_user_by_id(user_id)
    if not user:
        return False
    if user["plan"] == "free":
        return user["analysis_count"] < user["analysis_limit"]
    return True


# ---------- Analysis Operations ----------

def create_analysis(user_id, source_id, url, keyword, dimensions):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO analysis_tasks 
           (user_id, source_id, url, keyword, dimensions, status)
           VALUES (?, ?, ?, ?, ?, 'pending')""",
        (user_id, source_id, url, keyword, json.dumps(dimensions)),
    )
    conn.commit()
    task_id = cursor.lastrowid
    conn.close()
    return task_id


def update_analysis_result(task_id, status, result):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE analysis_tasks 
           SET status = ?, result_json = ?, completed_at = CURRENT_TIMESTAMP 
           WHERE id = ?""",
        (status, json.dumps(result, ensure_ascii=False), task_id),
    )
    conn.commit()
    conn.close()


def get_analysis(task_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM analysis_tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    if task:
        t = dict(task)
        t["dimensions"] = json.loads(t["dimensions"]) if t["dimensions"] else []
        t["result"] = json.loads(t["result_json"]) if t["result_json"] else None
        return t
    return None


def get_user_analyses(user_id, limit=20):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM analysis_tasks WHERE user_id = ? ORDER BY created_at DESC LIMIT ?",
        (user_id, limit),
    )
    tasks = [dict(row) for row in cursor.fetchall()]
    for t in tasks:
        t["dimensions"] = json.loads(t["dimensions"]) if t["dimensions"] else []
        t["result"] = json.loads(t["result_json"]) if t["result_json"] else None
    conn.close()
    return tasks


# ---------- Schedule Operations ----------

def create_schedule(user_id, task_id, interval_hours):
    next_run = datetime.now() + timedelta(hours=interval_hours)
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO schedules (user_id, task_id, interval_hours, next_run)
           VALUES (?, ?, ?, ?)""",
        (user_id, task_id, interval_hours, next_run.isoformat()),
    )
    conn.commit()
    schedule_id = cursor.lastrowid
    conn.close()
    return schedule_id


def get_user_schedules(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM schedules WHERE user_id = ? AND active = 1 ORDER BY next_run ASC",
        (user_id,),
    )
    schedules = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return schedules
