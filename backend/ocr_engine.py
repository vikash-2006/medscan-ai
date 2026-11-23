import re
import os
from typing import Dict, Any, List, Optional
from PIL import Image

try:
    import pytesseract
except ImportError:
    pytesseract = None

# Reference ranges for common medical lab tests
CLINICAL_REFERENCE_RANGES = {
    "blood_sugar": {"name": "Fasting Blood Sugar", "unit": "mg/dL", "min": 70, "max": 100, "warning_high": 126},
    "hba1c": {"name": "HbA1c (Glycated Hb)", "unit": "%", "min": 4.0, "max": 5.6, "warning_high": 6.5},
    "blood_pressure_sys": {"name": "Blood Pressure (Systolic)", "unit": "mmHg", "min": 90, "max": 120, "warning_high": 140},
    "blood_pressure_dia": {"name": "Blood Pressure (Diastolic)", "unit": "mmHg", "min": 60, "max": 80, "warning_high": 90},
    "cholesterol": {"name": "Total Cholesterol", "unit": "mg/dL", "min": 125, "max": 200, "warning_high": 240},
    "hemoglobin": {"name": "Hemoglobin", "unit": "g/dL", "min": 12.0, "max": 16.5, "warning_high": 18.0},
    "wbc": {"name": "Total WBC Count", "unit": "/cumm", "min": 4000, "max": 11000, "warning_high": 14000},
    "platelets": {"name": "Platelet Count", "unit": "lakh/cumm", "min": 1.5, "max": 4.5, "warning_high": 5.5},
    "bmi": {"name": "Body Mass Index (BMI)", "unit": "kg/m²", "min": 18.5, "max": 24.9, "warning_high": 30.0},
    "creatinine": {"name": "Serum Creatinine", "unit": "mg/dL", "min": 0.6, "max": 1.3, "warning_high": 1.8}
}

class OCREngine:
    def __init__(self, tesseract_cmd: Optional[str] = None):
        if tesseract_cmd and pytesseract:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd

    def extract_text(self, image_path: str) -> str:
        """
        Extracts raw text from image. If tesseract binary is not present,
        gracefully falls back or reads text embedded file.
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")

        # Check if pytesseract can run
        if pytesseract:
            try:
                img = Image.open(image_path)
                text = pytesseract.image_to_string(img)
                if text.strip():
                    return text
            except Exception as e:
                print(f"[OCR Warning] pytesseract extraction skipped/failed: {e}")

        # Fallback: Check if file has metadata or is a mock sample text
        try:
            txt_path = os.path.splitext(image_path)[0] + ".txt"
            if os.path.exists(txt_path):
                with open(txt_path, "r", encoding="utf-8", errors="ignore") as f:
                    return f.read()
        except Exception as e:
            print(f"[OCR Warning] text fallback read error: {e}")

        return ""

    def parse_biomarkers(self, text: str) -> Dict[str, Any]:
        """
        Uses resilient regular expressions to match medical biomarkers
        and evaluate against clinical standards.
        """
        found_markers: List[Dict[str, Any]] = []
        raw_values: Dict[str, float] = {}

        patterns = {
            "blood_sugar": [
                r"(?:fasting\s*(?:blood)?\s*(?:sugar|glucose)|glucose\s*fasting|fbs)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)",
                r"blood\s*sugar(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "hba1c": [
                r"(?:hba1c|glycated\s*hemoglobin|glyco\s*hb)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "blood_pressure": [
                r"(?:blood\s*pressure|b\.?p\.?)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]{2,3})\s*[\/|\\]\s*([0-9]{2,3})",
                r"sys(?:tolic)?(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]{2,3}).*?dia(?:stolic)?(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]{2,3})"
            ],
            "cholesterol": [
                r"(?:total\s*cholesterol|cholesterol\s*total|serum\s*cholesterol)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "hemoglobin": [
                r"(?:hemoglobin|haemoglobin|hb)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)\s*(?:g\/dl|gm%)?"
            ],
            "wbc": [
                r"(?:total\s*wbc|wbc\s*count|tlc|total\s*leucocyte\s*count)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "platelets": [
                r"(?:platelet\s*count|platelets)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "creatinine": [
                r"(?:serum\s*creatinine|creatinine)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "bmi": [
                r"(?:bmi|body\s*mass\s*index)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]+(?:\.[0-9]+)?)"
            ],
            "age": [
                r"(?:age|patient\s*age)(?:\s*\([^\)]+\))?[\s:\-–|]*([0-9]{1,3})\s*(?:y|yrs|years)?"
            ]
        }

        text_lower = text.lower()

        # Parse BP (special case: two numbers sys/dia)
        for bp_pattern in patterns["blood_pressure"]:
            match = re.search(bp_pattern, text_lower)
            if match:
                sys_val = float(match.group(1))
                dia_val = float(match.group(2))
                raw_values["blood_pressure_sys"] = sys_val
                raw_values["blood_pressure_dia"] = dia_val
                break

        # Parse remaining single-value biomarkers
        for key, regex_list in patterns.items():
            if key in ("blood_pressure",):
                continue
            for pat in regex_list:
                match = re.search(pat, text_lower)
                if match:
                    try:
                        raw_values[key] = float(match.group(1))
                        break
                    except ValueError:
                        pass

        # Evaluate each found biomarker against clinical reference ranges
        for key, val in raw_values.items():
            if key in CLINICAL_REFERENCE_RANGES:
                ref = CLINICAL_REFERENCE_RANGES[key]
                if val < ref["min"]:
                    status = "LOW"
                    badge_color = "amber"
                elif val > ref["max"]:
                    status = "HIGH"
                    badge_color = "red"
                else:
                    status = "NORMAL"
                    badge_color = "green"

                found_markers.append({
                    "key": key,
                    "name": ref["name"],
                    "value": val,
                    "unit": ref["unit"],
                    "reference_range": f"{ref['min']} - {ref['max']} {ref['unit']}",
                    "status": status,
                    "badge_color": badge_color
                })

        return {
            "biomarkers": found_markers,
            "raw_values": raw_values,
            "markers_count": len(found_markers),
            "abnormal_count": sum(1 for m in found_markers if m["status"] != "NORMAL")
        }
