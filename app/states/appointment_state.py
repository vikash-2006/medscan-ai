"""
Appointment state management module.
Handles booking, cancellation, and appointment history.
"""
import requests
from typing import Dict, Any, List


class AppointmentState:
    """Manages all appointment-related data and operations."""

    def __init__(self, patient_name: str, api_base_url: str):
        self.patient_name = patient_name
        self.api_base_url = api_base_url
        self.booked_appointments: List[Dict[str, Any]] = []
        self.selected_doctor: Dict[str, Any] = {
            "name": "Dr. Rohan Mehta",
            "specialty": "General Physician",
            "rating": "4.8",
            "reviews": "1,240",
            "experience": "7+ Years",
            "patients": "2.5K+",
            "avatar": "doctor_portrait.jpg",
            "fee": "₹500",
            "about": "Dr. Rohan Mehta is a Senior Consultant Physician specializing in internal medicine and preventive health."
        }
        self.medicines: List[Dict[str, Any]] = [
            {"name": "Metformin 500mg", "timing": "Morning • After Breakfast", "slot": "Morning", "taken": True},
            {"name": "Atorvastatin 10mg", "timing": "Night • Before Bed", "slot": "Night", "taken": False},
            {"name": "Telmisartan 40mg", "timing": "Morning • After Breakfast", "slot": "Morning", "taken": True},
            {"name": "Multivitamin & Zinc", "timing": "Afternoon • Post Lunch", "slot": "Afternoon", "taken": False},
        ]
        self._load_appointments()

    def _load_appointments(self):
        """Load appointments from SQLite DB with fallback."""
        try:
            from backend.database import get_appointments, save_appointment, init_db
            init_db()
            db_appts = get_appointments(limit=25)
            if db_appts:
                self.booked_appointments = db_appts
            else:
                save_appointment(
                    patient_name=self.patient_name,
                    doctor_name="Dr. Rohan Mehta",
                    specialty="General Physician • Consultation",
                    date_str="Tue, 17 Nov 2026",
                    time_str="11:00 AM",
                    fee="₹500", avatar="doctor_portrait.jpg", status="Confirmed"
                )
                self.booked_appointments = get_appointments(limit=25)
        except Exception:
            self.booked_appointments = [{
                "doctor_name": "Dr. Rohan Mehta",
                "specialty": "General Physician • Consultation",
                "date_str": "Tue, 17 Nov 2026",
                "time_str": "11:00 AM",
                "status": "Confirmed", "avatar": "doctor_portrait.jpg", "fee": "₹500"
            }]

    def book_appointment(self, doctor_name, specialty, date_str, time_str, fee="₹500", avatar="doctor_portrait.jpg"):
        """Book a new appointment with DB + API sync."""
        new_appt = {
            "patient_name": self.patient_name, "doctor_name": doctor_name,
            "specialty": specialty, "date_str": date_str, "time_str": time_str,
            "fee": fee, "avatar": avatar, "status": "Confirmed"
        }
        try:
            from backend.database import save_appointment
            appt_id = save_appointment(
                patient_name=self.patient_name, doctor_name=doctor_name,
                specialty=specialty, date_str=date_str, time_str=time_str,
                fee=fee, avatar=avatar, status="Confirmed"
            )
            new_appt["id"] = appt_id
        except Exception as e:
            print(f"[DB Warning] SQLite booking fallback: {e}")

        try:
            requests.post(f"{self.api_base_url}/api/appointments", json=new_appt, timeout=1.5)
        except Exception:
            pass

        self.booked_appointments.insert(0, new_appt)
        return new_appt

    def cancel_active_appointment(self, index: int = 0) -> bool:
        """Cancel an appointment by index."""
        if not self.booked_appointments or index >= len(self.booked_appointments):
            return False
        appt = self.booked_appointments[index]
        appt_id = appt.get("id")
        if appt_id:
            try:
                from backend.database import cancel_appointment
                cancel_appointment(appt_id)
            except Exception:
                pass
        self.booked_appointments.pop(index)
        return True
