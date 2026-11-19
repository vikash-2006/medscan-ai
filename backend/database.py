import sqlite3
import json
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medscan.db")

def get_key():
    key = os.getenv("ENCRYPTION_KEY")
    if not key:
        raise ValueError("ENCRYPTION_KEY not found in environment variables.")
    return key.encode()

fernet = Fernet(get_key())

def encrypt(data: str) -> str:
    return fernet.encrypt(data.encode()).decode()

def decrypt(data: str) -> str:
    return fernet.decrypt(data.encode()).decode()


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        raw_text TEXT,
        biomarkers TEXT,
        explanation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_assessments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT,
        vitals TEXT,
        predicted_risk TEXT,
        risk_probability REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS audit_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        level TEXT NOT NULL,
        category TEXT NOT NULL,
        action TEXT NOT NULL,
        details TEXT,
        ip_address TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_name TEXT NOT NULL,
        doctor_name TEXT NOT NULL,
        specialty TEXT NOT NULL,
        date_str TEXT NOT NULL,
        time_str TEXT NOT NULL,
        fee TEXT,
        avatar TEXT,
        status TEXT DEFAULT 'Confirmed',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

def save_report(title: str, raw_text: str, biomarkers: List[Dict[str, Any]], explanation: Dict[str, Any]) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO reports (title, raw_text, biomarkers, explanation)
        VALUES (?, ?, ?, ?)
    """, (title, raw_text, json.dumps(biomarkers), json.dumps(explanation)))
    report_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return report_id

def get_reports(limit: int = 20) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, title, raw_text, biomarkers, explanation, created_at 
        FROM reports 
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    reports = []
    for r in rows:
        reports.append({
            "id": r["id"],
            "title": r["title"],
            "raw_text": r["raw_text"],
            "biomarkers": json.loads(r["biomarkers"]) if r["biomarkers"] else [],
            "explanation": json.loads(r["explanation"]) if r["explanation"] else {},
            "created_at": r["created_at"]
        })
    return reports

def save_risk_assessment(patient_name: str, vitals: Dict[str, Any], risk: str, prob: float) -> int:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO risk_assessments (patient_name, vitals, predicted_risk, risk_probability)
        VALUES (?, ?, ?, ?)
    """, (patient_name, json.dumps(vitals), risk, prob))
    assessment_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return assessment_id

def get_risk_assessments(limit: int = 10) -> List[Dict[str, Any]]:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, patient_name, vitals, predicted_risk, risk_probability, created_at
        FROM risk_assessments
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    
    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "patient_name": r["patient_name"],
            "vitals": json.loads(r["vitals"]) if r["vitals"] else {},
            "predicted_risk": r["predicted_risk"],
            "risk_probability": r["risk_probability"],
            "created_at": r["created_at"]
        })
    return results

def insert_log(level: str, category: str, action: str, details: Optional[Dict[str, Any]] = None, ip_address: Optional[str] = None) -> int:
    """
    Stores an audit log event into the SQLite audit_logs table.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    details_str = json.dumps(details) if details else None
    cursor.execute("""
        INSERT INTO audit_logs (level, category, action, details, ip_address)
        VALUES (?, ?, ?, ?, ?)
    """, (level.upper(), category.upper(), action, details_str, ip_address or "127.0.0.1"))
    log_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return log_id

def get_audit_logs(limit: int = 50, category: Optional[str] = None, level: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Retrieves recent audit logs with optional category and level filtering.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    query = "SELECT id, timestamp, level, category, action, details, ip_address FROM audit_logs"
    params = []
    conditions = []
    
    if category:
        conditions.append("category = ?")
        params.append(category.upper())
    if level:
        conditions.append("level = ?")
        params.append(level.upper())
        
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
        
    query += " ORDER BY id DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, tuple(params))
    rows = cursor.fetchall()
    conn.close()
    
    logs = []
    for r in rows:
        details_val = None
        if r["details"]:
            try:
                details_val = json.loads(r["details"])
            except Exception:
                details_val = r["details"]
        logs.append({
            "id": r["id"],
            "timestamp": r["timestamp"],
            "level": r["level"],
            "category": r["category"],
            "action": r["action"],
            "details": details_val,
            "ip_address": r["ip_address"]
        })
    return logs

def save_appointment(patient_name: str, doctor_name: str, specialty: str, date_str: str, time_str: str, fee: str = "₹500", avatar: str = "doctor_portrait.jpg", status: str = "Confirmed") -> int:
    """
    Saves a booked doctor consultation appointment into SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO appointments (patient_name, doctor_name, specialty, date_str, time_str, fee, avatar, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (encrypt(patient_name), doctor_name, specialty, date_str, time_str, fee, avatar, status))
    appt_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return appt_id

def get_appointments(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Retrieves all booked doctor consultations from SQLite database.
    """
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, patient_name, doctor_name, specialty, date_str, time_str, fee, avatar, status, created_at
        FROM appointments
        ORDER BY id DESC LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()

    appointments = []
    for r in rows:
        appointments.append({
            "id": r["id"],
            "patient_name": decrypt(r["patient_name"]),
            "doctor_name": r["doctor_name"],
            "specialty": r["specialty"],
            "date_str": r["date_str"],
            "time_str": r["time_str"],
            "fee": r["fee"],
            "avatar": r["avatar"],
            "status": r["status"],
            "created_at": r["created_at"]
        })
    return appointments

def cancel_appointment(appointment_id: int) -> bool:
    """
    Cancels or removes an appointment from the database.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE appointments SET status = 'Cancelled' WHERE id = ?", (appointment_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_PATH)
