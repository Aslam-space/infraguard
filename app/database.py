import sqlite3
import os
from app.config import DB_PATH

def get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        cpu REAL, ram REAL, disk REAL,
        net_in REAL, net_out REAL, processes INTEGER)''')
    c.execute('''CREATE TABLE IF NOT EXISTS incidents (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        type TEXT, severity TEXT, metric_value REAL,
        action_taken TEXT, resolved INTEGER DEFAULT 0,
        mttr_seconds REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS healing_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        incident_id INTEGER, script_run TEXT,
        success INTEGER, output TEXT)''')
    conn.commit()
    conn.close()
    print("[DB] Tables ready")

def insert_metric(cpu, ram, disk, net_in, net_out, processes):
    conn = get_conn()
    conn.execute(
        'INSERT INTO metrics (cpu,ram,disk,net_in,net_out,processes) VALUES (?,?,?,?,?,?)',
        (cpu, ram, disk, net_in, net_out, processes))
    conn.commit()
    conn.close()

def insert_incident(type_, severity, metric_value, action_taken):
    conn = get_conn()
    c = conn.cursor()
    c.execute(
        'INSERT INTO incidents (type,severity,metric_value,action_taken) VALUES (?,?,?,?)',
        (type_, severity, metric_value, action_taken))
    incident_id = c.lastrowid
    conn.commit()
    conn.close()
    return incident_id

def resolve_incident(incident_id, mttr_seconds):
    conn = get_conn()
    conn.execute(
        'UPDATE incidents SET resolved=1, mttr_seconds=? WHERE id=?',
        (mttr_seconds, incident_id))
    conn.commit()
    conn.close()

def get_recent_metrics(limit=60):
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM metrics ORDER BY timestamp DESC LIMIT ?',
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_recent_incidents(limit=10):
    conn = get_conn()
    rows = conn.execute(
        'SELECT * FROM incidents ORDER BY timestamp DESC LIMIT ?',
        (limit,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_avg_mttr():
    conn = get_conn()
    row = conn.execute(
        'SELECT AVG(mttr_seconds) as avg FROM incidents WHERE resolved=1'
    ).fetchone()
    conn.close()
    return round(row['avg'] or 0, 1)
