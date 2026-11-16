import os
import sys

# Ensure root directory is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_full_user_flow():
    print("==================================================")
    print("  Running End-to-End Simulation: MedScan AI")
    print("==================================================")
    
    # 1. Read sample report
    sample_file = os.path.join(os.path.dirname(__file__), "sample_data", "sample_diabetes_lipid_report.txt")
    with open(sample_file, "r") as f:
        report_text = f.read()

    print("[Step 1] Sending sample medical report to /api/scan ...")
    scan_resp = client.post("/api/scan", data={"raw_text": report_text})
    assert scan_resp.status_code == 200
    scan_data = scan_resp.json()
    print(f"  ✓ Extracted {scan_data['markers_count']} biomarkers successfully.")
    for b in scan_data["biomarkers"]:
        print(f"    - {b['name']}: {b['value']} {b['unit']} ({b['status']})")

    print("\n[Step 2] Requesting AI clinical explanation in Hinglish ...")
    explain_resp = client.post("/api/explain", json={
        "title": "Vikash Kumawat - Lab Report",
        "raw_text": report_text,
        "biomarkers": scan_data["biomarkers"],
        "language": "hinglish"
    })
    assert explain_resp.status_code == 200
    expl = explain_resp.json()["explanation"]
    print(f"  ✓ Urgency Level: {expl['urgency_level']}")
    print(f"  ✓ Summary: {expl['summary']}")
    print("  ✓ Dietary Tips:")
    for tip in expl["diet_recommendations"]:
        print(f"    * {tip}")

    print("\n[Step 3] Running Sanjeevani ML Diagnostic Pipeline ...")
    raw_vals = scan_data["raw_values"]
    vitals = {
        "patient_name": "Vikash Kumawat",
        "age": 52.0,
        "blood_sugar": raw_vals.get("blood_sugar", 158.0),
        "blood_pressure_sys": raw_vals.get("blood_pressure_sys", 148.0),
        "blood_pressure_dia": raw_vals.get("blood_pressure_dia", 94.0),
        "bmi": raw_vals.get("bmi", 28.6),
        "cholesterol": raw_vals.get("cholesterol", 245.0),
        "hba1c": raw_vals.get("hba1c", 7.6)
    }
    risk_resp = client.post("/api/predict-risk", json=vitals)
    assert risk_resp.status_code == 200
    risk_data = risk_resp.json()
    print(f"  ✓ Predicted Risk Level: {risk_data['predicted_risk']}")
    print(f"  ✓ Model Confidence: {risk_data['confidence']}%")
    print(f"  ✓ Probabilities: {risk_data['probabilities']}")
    print(f"  ✓ Clinical Advice: {risk_data['clinical_advice']}")

    print("\n[Step 4] Verifying SQLite History ...")
    hist_resp = client.get("/api/history")
    assert hist_resp.status_code == 200
    hist = hist_resp.json()
    assert len(hist["reports"]) >= 1
    assert len(hist["risk_assessments"]) >= 1
    print(f"  ✓ History contains {len(hist['reports'])} reports and {len(hist['risk_assessments'])} risk assessments.")

    print("\n==================================================")
    print("  ALL E2E INTEGRATION TESTS PASSED 100%! 🎉")
    print("==================================================")

if __name__ == "__main__":
    test_full_user_flow()
