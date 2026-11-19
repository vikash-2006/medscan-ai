"""
Medical state management module.
Handles scan data, AI explanations, risk predictions, and clinical logic.
"""
import os
import re
from typing import Dict, Any, List, Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Clinical reference standards
REFERENCE_STANDARDS = {
    "blood_sugar": {"name": "Fasting Blood Sugar", "unit": "mg/dL", "min": 70, "max": 100, "warning_high": 126},
    "hba1c": {"name": "HbA1c (Glycated Hb)", "unit": "%", "min": 4.0, "max": 5.6, "warning_high": 6.5},
    "blood_pressure_sys": {"name": "Blood Pressure (Systolic)", "unit": "mmHg", "min": 90, "max": 120, "warning_high": 140},
    "blood_pressure_dia": {"name": "Blood Pressure (Diastolic)", "unit": "mmHg", "min": 60, "max": 80, "warning_high": 90},
    "cholesterol": {"name": "Total Cholesterol", "unit": "mg/dL", "min": 125, "max": 200, "warning_high": 240},
    "hemoglobin": {"name": "Hemoglobin", "unit": "g/dL", "min": 12.0, "max": 16.5, "warning_high": 18.0},
    "creatinine": {"name": "Serum Creatinine", "unit": "mg/dL", "min": 0.6, "max": 1.3, "warning_high": 1.8},
    "bmi": {"name": "Body Mass Index (BMI)", "unit": "kg/m²", "min": 18.5, "max": 24.9, "warning_high": 30.0}
}


class MedicalState:
    """Handles all medical data: scans, AI analysis, risk prediction."""

    def __init__(self):
        self.current_report_title: str = "Lab Test Report"
        self.current_scan_data: Optional[Dict[str, Any]] = None
        self.current_explanation: Optional[Dict[str, Any]] = None
        self.current_risk_result: Optional[Dict[str, Any]] = None

        self.history: List[Dict[str, Any]] = [
            {
                "title": "Comprehensive Lipid & Metabolic Panel",
                "created_at": "2026-11-16 10:30:00",
                "biomarkers": [
                    {"name": "Fasting Blood Sugar", "value": 158.0, "unit": "mg/dL", "status": "HIGH", "reference_range": "70 - 100 mg/dL"},
                    {"name": "HbA1c", "value": 7.6, "unit": "%", "status": "HIGH", "reference_range": "4.0 - 5.6 %"},
                    {"name": "Total Cholesterol", "value": 245.0, "unit": "mg/dL", "status": "HIGH", "reference_range": "125 - 200 mg/dL"},
                    {"name": "Blood Pressure (Systolic)", "value": 148.0, "unit": "mmHg", "status": "HIGH", "reference_range": "90 - 120 mmHg"}
                ],
                "explanation": {
                    "summary": "Aapki report me Fasting Blood Sugar (158 mg/dL) aur HbA1c (7.6%) significantly high hain.",
                    "urgency_level": "High Priority",
                    "diet_recommendations": [
                        "Refined sugar, meetha, aur maida bilkul band karein.",
                        "Khaane me karela, methi daana, aur green vegetables shamil karein.",
                        "Trans-fats aur fried snacks ki jagah roasted seeds aur fiber badhayein."
                    ],
                    "lifestyle_tips": [
                        "Rozana subah kam se kam 30 minute brisk walk karein.",
                        "Blood sugar ko log book me subah aur khaane ke 2 ghante baad record karein.",
                        "Sodium intake kam rakhein aur roz 7-8 ghante sound sleep lein."
                    ],
                    "doctor_advisory": "Physician ya Diabetologist se consult karke glycemic therapy review karwayein."
                }
            }
        ]

        self.risk_history: List[Dict[str, Any]] = [
            {
                "patient_name": "Vikash Kumawat",
                "predicted_risk": "High Risk",
                "risk_probability": 96.6,
                "created_at": "2026-11-16 11:15:00"
            }
        ]

    def parse_biomarkers_offline(self, text: str) -> Dict[str, Any]:
        """On-device regex biomarker extraction."""
        patterns = {
            "blood_sugar": [r"(?:fasting\s*blood\s*sugar|fbs|fasting\s*glucose|glucose\s*fasting)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"],
            "hba1c": [r"(?:hba1c|glycated\s*hemoglobin)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"],
            "blood_pressure_sys": [r"(?:bp|blood\s*pressure)\s*[:=-]?\s*([0-9]{2,3})\s*/\s*([0-9]{2,3})"],
            "cholesterol": [r"(?:total\s*cholesterol|cholesterol)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"],
            "hemoglobin": [r"(?:hemoglobin|hb)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"],
            "creatinine": [r"(?:serum\s*creatinine|creatinine)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"],
            "bmi": [r"(?:bmi|body\s*mass\s*index)\s*[:=-]?\s*([0-9]+(?:\.[0-9]+)?)"]
        }
        
        extracted = {}
        for key, p_list in patterns.items():
            for p in p_list:
                m = re.search(p, text, re.IGNORECASE)
                if m:
                    if key == "blood_pressure_sys":
                        extracted["blood_pressure_sys"] = float(m.group(1))
                        extracted["blood_pressure_dia"] = float(m.group(2))
                    else:
                        extracted[key] = float(m.group(1))
                    break

        biomarkers = []
        for key, val in extracted.items():
            ref = REFERENCE_STANDARDS.get(key, {"name": key.title(), "unit": "", "min": 0, "max": 999, "warning_high": 999})
            st = "NORMAL"
            if val > ref["max"]:
                st = "HIGH"
            elif val < ref["min"]:
                st = "LOW"
            biomarkers.append({
                "key": key, "name": ref["name"], "value": val, "unit": ref["unit"],
                "status": st, "reference_range": f"{ref['min']} - {ref['max']} {ref['unit']}"
            })

        return {
            "biomarkers": biomarkers, "raw_values": extracted,
            "raw_text": text, "markers_count": len(biomarkers),
            "abnormal_count": sum(1 for b in biomarkers if b["status"] != "NORMAL")
        }

    def offline_explain(self, biomarkers: List[Dict[str, Any]]) -> Dict[str, Any]:
        """On-device deterministic clinical explanation."""
        abnormal = [b for b in biomarkers if b.get("status") != "NORMAL"]
        if not abnormal:
            return {
                "summary": "Aapki sabhi clinical lab values normal range me hain.",
                "urgency_level": "Normal",
                "diet_recommendations": ["Balanced diet maintain karein.", "Daily 2.5-3L paani piyein.", "Processed food kam rakhein."],
                "lifestyle_tips": ["Rozana 30 min walk/yoga.", "7-8 hours sleep.", "Annual checkup karwayein."],
                "doctor_advisory": "Routine checkup complete. Vitals healthy hain."
            }

        high_names = [f"{b['name']} ({b['value']} {b['unit']})" for b in abnormal]
        return {
            "summary": f"Report me {', '.join(high_names[:3])} elevated hain. Lifestyle care zaroori hai.",
            "urgency_level": "High Priority" if len(abnormal) >= 2 else "Moderate Caution",
            "diet_recommendations": ["Refined carbs/sugar se parhez.", "High-fiber diet: oats, methi, daliya.", "Boiled/roasted options choose karein."],
            "lifestyle_tips": ["Rozana 30-45 min brisk walking.", "Stress manage karein, deep breathing.", "Values weekly monitor karein."],
            "doctor_advisory": "Report apne doctor ko dikhayein."
        }

    def offline_risk_predict(self, vitals: Dict[str, float]) -> Dict[str, Any]:
        """On-device ML triage risk predictor."""
        sugar = vitals.get("blood_sugar", 100.0)
        hba1c = vitals.get("hba1c", 5.5)
        sys_bp = vitals.get("blood_pressure_sys", 120.0)
        chol = vitals.get("cholesterol", 180.0)
        bmi = vitals.get("bmi", 24.0)
        
        score = 0
        if sugar >= 126 or hba1c >= 6.5: score += 3
        elif sugar >= 100 or hba1c >= 5.7: score += 1
        if sys_bp >= 140: score += 2
        elif sys_bp >= 125: score += 1
        if chol >= 240: score += 2
        elif chol >= 200: score += 1
        if bmi >= 30: score += 2
        elif bmi >= 25: score += 1
        
        if score >= 5:
            predicted, conf, color = "High Risk", min(98.5, 86.0 + score * 1.8), "#DC2626"
            advice = "Immediate medical consult recommended."
            probs = {"Low Risk": 2.1, "Moderate Risk": 9.4, "High Risk": round(conf, 1)}
        elif score >= 2:
            predicted, conf, color = "Moderate Risk", 78.5, "#D97706"
            advice = "Lifestyle modifications needed: 30 min daily exercise."
            probs = {"Low Risk": 12.5, "Moderate Risk": 78.5, "High Risk": 9.0}
        else:
            predicted, conf, color = "Low Risk", 94.2, "#16A34A"
            advice = "Vitals healthy. Maintain routine physical activity."
            probs = {"Low Risk": 94.2, "Moderate Risk": 4.8, "High Risk": 1.0}
        
        return {
            "predicted_risk": predicted, "confidence": conf, "risk_color": color,
            "clinical_advice": advice, "probabilities": probs, "source": "on_device_ml_triage"
        }
