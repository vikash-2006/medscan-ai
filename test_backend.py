from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def run_tests():
    print("Testing /api/health...")
    r = client.get("/api/health")
    assert r.status_code == 200, f"Health check failed: {r.text}"
    print("  -> Health OK:", r.json())

    print("\nTesting /api/scan with simulated lab report text...")
    sample_text = """
    CENTRAL CLINICAL PATHOLOGY LAB
    Patient Name: Rahul Verma    Age: 52 Yrs
    -------------------------------------------
    TEST DESCRIPTION               RESULT     NORMAL RANGE
    Fasting Blood Sugar (FBS)      142 mg/dL  (70 - 100)
    HbA1c Glycated Hemoglobin      7.2 %      (4.0 - 5.6)
    Blood Pressure (BP)            145/92     (120/80)
    Total Cholesterol              235 mg/dL  (125 - 200)
    Hemoglobin (Hb)                14.2 g/dL  (12.0 - 16.5)
    Serum Creatinine               1.0 mg/dL  (0.6 - 1.3)
    """
    r = client.post("/api/scan", data={"raw_text": sample_text})
    assert r.status_code == 200, f"Scan failed: {r.text}"
    scan_res = r.json()
    print(f"  -> Extracted {scan_res['markers_count']} markers ({scan_res['abnormal_count']} abnormal)")
    for m in scan_res["biomarkers"]:
        print(f"     [{m['status']}] {m['name']}: {m['value']} {m['unit']}")

    print("\nTesting /api/explain...")
    r = client.post("/api/explain", json={
        "title": "Rahul Verma - Lipid & Sugar Report",
        "raw_text": sample_text,
        "biomarkers": scan_res["biomarkers"],
        "language": "hinglish"
    })
    assert r.status_code == 200, f"Explain failed: {r.text}"
    exp_res = r.json()
    print("  -> Summary:", exp_res["explanation"]["summary"])
    print("  -> Urgency:", exp_res["explanation"]["urgency_level"])
    print("  -> Key Findings Count:", len(exp_res["explanation"]["key_findings"]))

    print("\nTesting /api/predict-risk (Sanjeevani ML Engine)...")
    vitals = {
        "patient_name": "Rahul Verma",
        "age": 52,
        "blood_sugar": 142,
        "blood_pressure_sys": 145,
        "blood_pressure_dia": 92,
        "bmi": 28.4,
        "cholesterol": 235,
        "hba1c": 7.2
    }
    r = client.post("/api/predict-risk", json=vitals)
    assert r.status_code == 200, f"Predict risk failed: {r.text}"
    risk_res = r.json()
    print("  -> Predicted Risk:", risk_res["predicted_risk"])
    print("  -> Confidence:", risk_res["confidence"], "%")
    print("  -> Probabilities:", risk_res["probabilities"])

    print("\nTesting /api/history...")
    r = client.get("/api/history")
    assert r.status_code == 200
    hist = r.json()
    print(f"  -> Saved reports: {len(hist['reports'])}, Saved risk checks: {len(hist['risk_assessments'])}")

    print("\nTesting /api/chat (Conversational Logger)...")
    r = client.post("/api/chat", json={"message": "I have high blood sugar, what should I eat?", "patient_name": "Vikash"})
    assert r.status_code == 200
    chat_res = r.json()
    print(f"  -> Chat response: {chat_res['reply']}")

    print("\nTesting /api/logs (Audit Logs & File Log Tail)...")
    r = client.get("/api/logs?limit=10")
    assert r.status_code == 200
    log_res = r.json()
    print(f"  -> Total Database Logs Stored: {log_res['total_database_logs']}")
    print(f"  -> Log file path: {log_res['log_file_path']}")
    print(f"  -> Recent audit logs count: {len(log_res['audit_logs'])}")
    if log_res["audit_logs"]:
        latest = log_res["audit_logs"][0]
        print(f"     Latest Log: [{latest['timestamp']}] [{latest['level']}] [{latest['category']}] {latest['action']}")
    print(f"  -> File log tail lines count: {len(log_res['file_log_tail'])}")

    print("\nALL BACKEND API & LOGGING TESTS PASSED SUCCESSFULLY! 🎉")

if __name__ == "__main__":
    run_tests()
