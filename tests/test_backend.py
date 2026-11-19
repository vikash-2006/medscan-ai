import sys
import os
# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from backend.database import save_appointment, get_appointments, encrypt, decrypt, init_db

# Ensure a fresh test DB
TEST_DB = "test_medscan.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
import backend.database
backend.database.DB_PATH = TEST_DB
init_db()

def test_encryption():
    data = "Vikash Kumawat"
    encrypted = encrypt(data)
    assert encrypted != data
    decrypted = decrypt(encrypted)
    assert decrypted == data

def test_appointment_booking():
    save_appointment("Vikash Kumawat", "Dr. Rohan Mehta", "General", "2026-11-20", "10:00 AM")
    appointments = get_appointments()
    assert len(appointments) == 1
    assert appointments[0]["patient_name"] == "Vikash Kumawat"
    assert appointments[0]["doctor_name"] == "Dr. Rohan Mehta"
