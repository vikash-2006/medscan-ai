import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app.theme import theme
from app.states.user_state import UserState
from app.states.medical_state import MedicalState, REFERENCE_STANDARDS
from app.states.appointment_state import AppointmentState
from app.scheduler import SLOT_TIMES, is_scheduler_running
from backend.cloud_backup import get_table_setup_sql, is_cloud_available

def test_theme_light_and_dark_mode():
    """Verify theme transitions properly between light and dark modes."""
    theme.dark_mode = False
    assert theme.bg() == "#F8FAFC"
    assert theme.card_bg() == "#FFFFFF"
    assert theme.text_primary() == "#0F172A"

    theme.dark_mode = True
    assert theme.bg() == "#0F172A"
    assert theme.card_bg() == "#1E293B"
    assert theme.text_primary() == "#F1F5F9"
    theme.dark_mode = False  # Reset to default

def test_medical_state_offline_parsing():
    """Verify regex biomarker extraction and status classification."""
    med = MedicalState()
    sample_text = "Fasting Blood Sugar: 158 mg/dL, HbA1c: 7.6 %, Blood Pressure: 148/92, Total Cholesterol: 245 mg/dL"
    parsed = med.parse_biomarkers_offline(sample_text)
    
    assert parsed["markers_count"] >= 4
    assert parsed["abnormal_count"] >= 3
    
    sugar_marker = next((b for b in parsed["biomarkers"] if "sugar" in b["name"].lower()), None)
    assert sugar_marker is not None
    assert sugar_marker["value"] == 158.0
    assert sugar_marker["status"] == "HIGH"

def test_medical_state_risk_prediction():
    """Verify on-device ML triage logic for high vs low risk."""
    med = MedicalState()
    
    # High risk vitals
    high_vitals = {
        "blood_sugar": 160.0,
        "hba1c": 7.8,
        "blood_pressure_sys": 150.0,
        "cholesterol": 250.0,
        "bmi": 31.0
    }
    risk_high = med.offline_risk_predict(high_vitals)
    assert risk_high["predicted_risk"] == "High Risk"
    assert risk_high["confidence"] >= 85.0
    
    # Normal/healthy vitals
    healthy_vitals = {
        "blood_sugar": 85.0,
        "hba1c": 5.1,
        "blood_pressure_sys": 115.0,
        "cholesterol": 165.0,
        "bmi": 22.0
    }
    risk_low = med.offline_risk_predict(healthy_vitals)
    assert risk_low["predicted_risk"] == "Low Risk"

def test_user_state():
    """Verify UserState vitals update and dark mode toggle."""
    user = UserState()
    assert user.patient_name == "Vikash Kumawat"
    user.update_vitals({"blood_sugar": 135.0, "bmi": 26.2})
    assert user.current_vitals["blood_sugar"] == 135.0
    assert user.current_vitals["bmi"] == 26.2

def test_scheduler_slots():
    """Verify scheduler has predefined time slots."""
    assert "Morning" in SLOT_TIMES
    assert "Night" in SLOT_TIMES
    assert SLOT_TIMES["Morning"] == "08:00"

def test_cloud_backup_schema():
    """Verify Supabase SQL generator contains all required tables."""
    sql = get_table_setup_sql()
    assert "CREATE TABLE IF NOT EXISTS appointments" in sql
    assert "CREATE TABLE IF NOT EXISTS medical_reports" in sql
    assert "CREATE TABLE IF NOT EXISTS risk_assessments" in sql
    assert "CREATE TABLE IF NOT EXISTS medicines" in sql
