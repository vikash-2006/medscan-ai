"""
Cloud Backup Module for MedScan AI.
Syncs local SQLite data to Supabase (PostgreSQL cloud).
Supports: Appointments, Reports, Risk Assessments, Medicine Lists.

Setup:
1. Create free account at https://supabase.com
2. Create a new project
3. Add SUPABASE_URL and SUPABASE_KEY to .env file
4. Run the SQL from create_tables() in Supabase SQL Editor
"""
import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

_supabase_client = None
_cloud_available = False


def _init_supabase():
    """Initialize Supabase client lazily."""
    global _supabase_client, _cloud_available
    
    if _supabase_client is not None:
        return _cloud_available
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")
    
    if not url or not key:
        print("[Cloud] SUPABASE_URL/SUPABASE_KEY not found in .env. Cloud backup disabled.")
        _cloud_available = False
        return False
    
    try:
        from supabase import create_client
        _supabase_client = create_client(url, key)
        _cloud_available = True
        print("[Cloud] ✅ Supabase connected successfully!")
        return True
    except ImportError:
        print("[Cloud] supabase-py not installed. Run: pip install supabase")
        _cloud_available = False
        return False
    except Exception as e:
        print(f"[Cloud] ❌ Supabase connection failed: {e}")
        _cloud_available = False
        return False


def is_cloud_available() -> bool:
    """Check if cloud backup is configured and available."""
    _init_supabase()
    return _cloud_available


def get_table_setup_sql() -> str:
    """Returns SQL to create required tables in Supabase."""
    return """
-- Run this in Supabase SQL Editor (one time setup)

CREATE TABLE IF NOT EXISTS appointments (
    id SERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    doctor_name TEXT NOT NULL,
    specialty TEXT,
    date_str TEXT,
    time_str TEXT,
    fee TEXT DEFAULT '₹500',
    avatar TEXT DEFAULT 'doctor_portrait.jpg',
    status TEXT DEFAULT 'Confirmed',
    device_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS medical_reports (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    biomarkers JSONB,
    explanation JSONB,
    raw_text TEXT,
    markers_count INT DEFAULT 0,
    abnormal_count INT DEFAULT 0,
    device_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS risk_assessments (
    id SERIAL PRIMARY KEY,
    patient_name TEXT NOT NULL,
    predicted_risk TEXT,
    risk_probability FLOAT,
    vitals JSONB,
    clinical_advice TEXT,
    device_id TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS medicines (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    timing TEXT,
    slot TEXT,
    taken BOOLEAN DEFAULT FALSE,
    device_id TEXT,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE appointments ENABLE ROW LEVEL SECURITY;
ALTER TABLE medical_reports ENABLE ROW LEVEL SECURITY;
ALTER TABLE risk_assessments ENABLE ROW LEVEL SECURITY;
ALTER TABLE medicines ENABLE ROW LEVEL SECURITY;
"""


def _get_device_id() -> str:
    """Generate a unique device identifier for syncing."""
    import hashlib
    import platform
    raw = f"{platform.node()}-{platform.system()}-{os.getenv('USER', 'medscan')}"
    return hashlib.md5(raw.encode()).hexdigest()[:12]


# =========================================================
# BACKUP (Local → Cloud)
# =========================================================

def backup_appointments(appointments: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Upload local appointments to Supabase cloud."""
    if not _init_supabase():
        return {"success": False, "error": "Cloud not available"}
    
    device_id = _get_device_id()
    uploaded = 0
    errors = 0
    
    for appt in appointments:
        try:
            record = {
                "patient_name": appt.get("patient_name", ""),
                "doctor_name": appt.get("doctor_name", ""),
                "specialty": appt.get("specialty", ""),
                "date_str": appt.get("date_str", ""),
                "time_str": appt.get("time_str", ""),
                "fee": appt.get("fee", "₹500"),
                "avatar": appt.get("avatar", ""),
                "status": appt.get("status", "Confirmed"),
                "device_id": device_id,
            }
            _supabase_client.table("appointments").upsert(record).execute()
            uploaded += 1
        except Exception as e:
            print(f"[Cloud] Appointment backup error: {e}")
            errors += 1
    
    return {"success": True, "uploaded": uploaded, "errors": errors}


def backup_reports(history: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Upload scan history/reports to Supabase cloud."""
    if not _init_supabase():
        return {"success": False, "error": "Cloud not available"}
    
    device_id = _get_device_id()
    uploaded = 0
    
    for report in history:
        try:
            record = {
                "title": report.get("title", "Lab Report"),
                "biomarkers": json.dumps(report.get("biomarkers", [])),
                "explanation": json.dumps(report.get("explanation", {})),
                "raw_text": report.get("raw_text", ""),
                "markers_count": len(report.get("biomarkers", [])),
                "abnormal_count": sum(1 for b in report.get("biomarkers", []) if b.get("status") != "NORMAL"),
                "device_id": device_id,
                "created_at": report.get("created_at", datetime.now().isoformat()),
            }
            _supabase_client.table("medical_reports").insert(record).execute()
            uploaded += 1
        except Exception as e:
            print(f"[Cloud] Report backup error: {e}")
    
    return {"success": True, "uploaded": uploaded}


def backup_risk_history(risk_history: List[Dict[str, Any]], vitals: Dict[str, float] = None) -> Dict[str, Any]:
    """Upload risk assessments to Supabase cloud."""
    if not _init_supabase():
        return {"success": False, "error": "Cloud not available"}
    
    device_id = _get_device_id()
    uploaded = 0
    
    for risk in risk_history:
        try:
            record = {
                "patient_name": risk.get("patient_name", ""),
                "predicted_risk": risk.get("predicted_risk", ""),
                "risk_probability": risk.get("risk_probability", 0),
                "vitals": json.dumps(vitals or {}),
                "clinical_advice": risk.get("clinical_advice", ""),
                "device_id": device_id,
                "created_at": risk.get("created_at", datetime.now().isoformat()),
            }
            _supabase_client.table("risk_assessments").insert(record).execute()
            uploaded += 1
        except Exception as e:
            print(f"[Cloud] Risk backup error: {e}")
    
    return {"success": True, "uploaded": uploaded}


def backup_medicines(medicines: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Upload medicine list to Supabase cloud."""
    if not _init_supabase():
        return {"success": False, "error": "Cloud not available"}
    
    device_id = _get_device_id()
    
    # Clear old medicines for this device, then insert fresh
    try:
        _supabase_client.table("medicines").delete().eq("device_id", device_id).execute()
    except Exception:
        pass
    
    uploaded = 0
    for med in medicines:
        try:
            record = {
                "name": med.get("name", ""),
                "timing": med.get("timing", ""),
                "slot": med.get("slot", "Morning"),
                "taken": med.get("taken", False),
                "device_id": device_id,
            }
            _supabase_client.table("medicines").insert(record).execute()
            uploaded += 1
        except Exception as e:
            print(f"[Cloud] Medicine backup error: {e}")
    
    return {"success": True, "uploaded": uploaded}


def full_backup(state) -> Dict[str, Any]:
    """
    One-click full backup of all data.
    Pass the app state object.
    """
    if not _init_supabase():
        return {"success": False, "error": "Cloud backup not configured. Add SUPABASE_URL and SUPABASE_KEY to .env"}
    
    results = {}
    
    try:
        results["appointments"] = backup_appointments(state.booked_appointments)
    except Exception as e:
        results["appointments"] = {"success": False, "error": str(e)}
    
    try:
        results["reports"] = backup_reports(state.history)
    except Exception as e:
        results["reports"] = {"success": False, "error": str(e)}
    
    try:
        results["risk"] = backup_risk_history(state.risk_history, state.current_vitals)
    except Exception as e:
        results["risk"] = {"success": False, "error": str(e)}
    
    try:
        results["medicines"] = backup_medicines(state.medicines)
    except Exception as e:
        results["medicines"] = {"success": False, "error": str(e)}
    
    total_uploaded = sum(r.get("uploaded", 0) for r in results.values() if isinstance(r, dict))
    total_errors = sum(r.get("errors", 0) for r in results.values() if isinstance(r, dict))
    
    return {
        "success": True,
        "total_uploaded": total_uploaded,
        "total_errors": total_errors,
        "details": results,
        "timestamp": datetime.now().isoformat()
    }


# =========================================================
# RESTORE (Cloud → Local)
# =========================================================

def restore_appointments() -> List[Dict[str, Any]]:
    """Download appointments from Supabase cloud."""
    if not _init_supabase():
        return []
    
    try:
        device_id = _get_device_id()
        response = _supabase_client.table("appointments") \
            .select("*") \
            .eq("device_id", device_id) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()
        return response.data or []
    except Exception as e:
        print(f"[Cloud] Restore appointments error: {e}")
        return []


def restore_reports() -> List[Dict[str, Any]]:
    """Download medical reports from Supabase cloud."""
    if not _init_supabase():
        return []
    
    try:
        device_id = _get_device_id()
        response = _supabase_client.table("medical_reports") \
            .select("*") \
            .eq("device_id", device_id) \
            .order("created_at", desc=True) \
            .limit(50) \
            .execute()
        
        reports = []
        for r in (response.data or []):
            report = {
                "title": r.get("title", ""),
                "created_at": r.get("created_at", ""),
                "biomarkers": json.loads(r["biomarkers"]) if isinstance(r.get("biomarkers"), str) else r.get("biomarkers", []),
                "explanation": json.loads(r["explanation"]) if isinstance(r.get("explanation"), str) else r.get("explanation", {}),
            }
            reports.append(report)
        return reports
    except Exception as e:
        print(f"[Cloud] Restore reports error: {e}")
        return []


def restore_medicines() -> List[Dict[str, Any]]:
    """Download medicine list from Supabase cloud."""
    if not _init_supabase():
        return []
    
    try:
        device_id = _get_device_id()
        response = _supabase_client.table("medicines") \
            .select("*") \
            .eq("device_id", device_id) \
            .execute()
        
        return [{
            "name": m.get("name", ""),
            "timing": m.get("timing", ""),
            "slot": m.get("slot", "Morning"),
            "taken": m.get("taken", False)
        } for m in (response.data or [])]
    except Exception as e:
        print(f"[Cloud] Restore medicines error: {e}")
        return []


def full_restore(state) -> Dict[str, Any]:
    """
    One-click full restore of all data from cloud.
    Merges cloud data into local state.
    """
    if not _init_supabase():
        return {"success": False, "error": "Cloud not configured"}
    
    restored = {}
    
    try:
        cloud_appts = restore_appointments()
        if cloud_appts:
            state.booked_appointments = cloud_appts
            restored["appointments"] = len(cloud_appts)
    except Exception as e:
        restored["appointments_error"] = str(e)
    
    try:
        cloud_reports = restore_reports()
        if cloud_reports:
            state.history = cloud_reports
            restored["reports"] = len(cloud_reports)
    except Exception as e:
        restored["reports_error"] = str(e)
    
    try:
        cloud_meds = restore_medicines()
        if cloud_meds:
            state.medicines = cloud_meds
            restored["medicines"] = len(cloud_meds)
    except Exception as e:
        restored["medicines_error"] = str(e)
    
    return {"success": True, "restored": restored, "timestamp": datetime.now().isoformat()}
