
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI(title="ai-log-insight API", version="0.2.0")
DB_PATH = "/data/logs.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        level TEXT,
        service TEXT,
        message TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

class LogEntry(BaseModel):
    timestamp: str
    level: str
    service: str
    message: str

@app.get("/health")
def health():
    return {"status": "ok", "version": "0.2.0"}

@app.post("/logs")
def ingest_log(log: LogEntry):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (timestamp, level, service, message) VALUES (?, ?, ?, ?)",
        (log.timestamp, log.level, log.service, log.message)
    )
    conn.commit()
    conn.close()
    return {"status": "stored"}

@app.get("/logs/search")
def search_logs(level: str | None = None, service: str | None = None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    query = "SELECT timestamp, level, service, message FROM logs WHERE 1=1"
    params = []
    if level:
        query += " AND level=?"
        params.append(level)
    if service:
        query += " AND service=?"
        params.append(service)
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return [
        {"timestamp": r[0], "level": r[1], "service": r[2], "message": r[3]}
        for r in rows
    ]
