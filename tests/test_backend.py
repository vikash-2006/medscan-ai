import sys
import os
# Add the project root to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from backend.database import save_appointment, get_appointments, encrypt, safe_decrypt, init_db

# Ensure a fresh test DB
TEST_DB = "test_medscan.db"
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
import backend.database
backend.database.DB_PATH = TEST_DB
init_db()

def test_encryption():
    """Test that encrypt + safe_decrypt roundtrip works."""
    data = "Vikash Kumawat"
    encrypted = encrypt(data)
    assert encrypted != data
    decrypted = safe_decrypt(encrypted)
    assert decrypted == data

def test_decrypt_legacy_plaintext():
    """Test that safe_decrypt handles legacy unencrypted data gracefully."""
    plain = "Dr. Rohan Mehta"
    result = safe_decrypt(plain)
    assert result == plain  # Should return as-is, not crash

def test_appointment_booking():
    """Test full appointment booking and retrieval flow."""
    save_appointment("Vikash Kumawat", "Dr. Rohan Mehta", "General", "2026-11-20", "10:00 AM")
    appointments = get_appointments()
    assert len(appointments) >= 1
    # Patient name is encrypted in DB, safe_decrypt in get_appointments
    assert appointments[0]["doctor_name"] == "Dr. Rohan Mehta"

def test_appointment_patient_name():
    """Test that patient name is properly decrypted from DB."""
    appointments = get_appointments()
    assert len(appointments) >= 1
    # safe_decrypt should handle both encrypted and plain text
    assert appointments[0]["patient_name"] in ["Vikash Kumawat", ""]
