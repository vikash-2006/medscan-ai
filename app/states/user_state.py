"""
User state management module.
Handles user profile, patient info, and personal settings.
"""
from typing import Dict, Any

class UserState:
    """Manages user profile and personal information."""
    
    def __init__(self):
        self.patient_name: str = "Vikash Kumawat"
        self.dark_mode: bool = False
        self.current_vitals: Dict[str, float] = {
            "age": 45.0,
            "blood_sugar": 120.0,
            "blood_pressure_sys": 130.0,
            "blood_pressure_dia": 85.0,
            "bmi": 25.5,
            "cholesterol": 210.0,
            "hba1c": 6.0
        }

    def update_vitals(self, vitals: Dict[str, float]):
        """Safely update vitals with new values."""
        for k, v in vitals.items():
            if k in self.current_vitals:
                try:
                    self.current_vitals[k] = float(v)
                except (ValueError, TypeError):
                    pass

    def toggle_dark_mode(self) -> bool:
        """Toggle dark mode and return new state."""
        self.dark_mode = not self.dark_mode
        return self.dark_mode
