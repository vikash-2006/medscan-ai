import os
import requests
from typing import Dict, Any, List, Optional

class AppState:
    def __init__(self, api_base_url: str = "http://127.0.0.1:8000"):
        self.api_base_url = api_base_url
        self.current_report_title = "Lab Test Report"
        self.current_scan_data: Optional[Dict[str, Any]] = None
        self.current_explanation: Optional[Dict[str, Any]] = None
        self.current_risk_result: Optional[Dict[str, Any]] = None
        self.current_vitals: Dict[str, float] = {
            "age": 45.0,
            "blood_sugar": 120.0,
            "blood_pressure_sys": 130.0,
            "blood_pressure_dia": 85.0,
            "bmi": 25.5,
            "cholesterol": 210.0,
            "hba1c": 6.0
        }
        self.patient_name = "Vikash Kumawat"
        self.history: List[Dict[str, Any]] = []

    def check_backend_connection(self) -> bool:
        try:
            r = requests.get(f"{self.api_base_url}/api/health", timeout=2)
            return r.status_code == 200
        except Exception:
            return False

    def scan_medical_report(self, image_path: Optional[str] = None, raw_text: Optional[str] = None) -> Dict[str, Any]:
        """
        Sends image or raw text to backend for OCR + biomarker parsing.
        """
        url = f"{self.api_base_url}/api/scan"
        if image_path and os.path.exists(image_path):
            with open(image_path, "rb") as f:
                files = {"file": (os.path.basename(image_path), f, "image/jpeg")}
                data = {"raw_text": raw_text or ""}
                resp = requests.post(url, files=files, data=data, timeout=30)
        else:
            resp = requests.post(url, data={"raw_text": raw_text or ""}, timeout=30)
            
        if resp.status_code == 200:
            self.current_scan_data = resp.json()
            # Auto-update vitals from parsed scan markers if available
            raw_vals = self.current_scan_data.get("raw_values", {})
            for key in self.current_vitals.keys():
                if key in raw_vals:
                    self.current_vitals[key] = float(raw_vals[key])
            return self.current_scan_data
        else:
            raise RuntimeError(f"Scan API failed with code {resp.status_code}: {resp.text}")

    def generate_ai_explanation(self, language: str = "hinglish") -> Dict[str, Any]:
        if not self.current_scan_data or not self.current_scan_data.get("biomarkers"):
            raise ValueError("No biomarkers available to explain. Scan a report first.")

        url = f"{self.api_base_url}/api/explain"
        payload = {
            "title": self.current_report_title,
            "raw_text": self.current_scan_data.get("raw_text", ""),
            "biomarkers": self.current_scan_data.get("biomarkers", []),
            "language": language,
            "save_to_history": True
        }
        resp = requests.post(url, json=payload, timeout=45)
        if resp.status_code == 200:
            res_data = resp.json()
            self.current_explanation = res_data.get("explanation", {})
            return self.current_explanation
        else:
            raise RuntimeError(f"Explain API failed: {resp.text}")

    def predict_sanjeevani_risk(self, vitals: Optional[Dict[str, float]] = None) -> Dict[str, Any]:
        url = f"{self.api_base_url}/api/predict-risk"
        if vitals:
            self.current_vitals.update(vitals)
            
        payload = {
            "patient_name": self.patient_name,
            **self.current_vitals
        }
        resp = requests.post(url, json=payload, timeout=15)
        if resp.status_code == 200:
            self.current_risk_result = resp.json()
            return self.current_risk_result
        else:
            raise RuntimeError(f"Risk prediction API failed: {resp.text}")

    def load_history(self) -> Dict[str, Any]:
        try:
            resp = requests.get(f"{self.api_base_url}/api/history", timeout=10)
            if resp.status_code == 200:
                data = resp.json()
                self.history = data.get("reports", [])
                return data
        except Exception as e:
            print(f"[History Error]: {e}")
        return {"reports": [], "risk_assessments": []}

state = AppState()
