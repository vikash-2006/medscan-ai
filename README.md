# MedScan AI (Sanjeevani Pocket) 🏥📱

> **End-to-End Python-based Android Mobile App for Medical Report OCR, GenAI Clinical Insights, & Healthcare ML Diagnostics.**

---

## 📌 Executive Summary & Resume Alignment

MedScan AI integrates two core industry-grade systems into a production-style cross-platform Android mobile application:
1. **Multimodal Document Intelligence & OCR Pipeline:** Scans prescriptions and clinical laboratory reports (CBC, Lipid profile, Fasting Glucose, HbA1c), extracts biomarkers with regularized normalization, and translates complex medical parameters into empathetic, patient-friendly **Hinglish/English** clinical summaries using **Generative AI (Groq LLM / Clinical NLP Engine)**.
2. **Sanjeevani Diagnostic ML System:** Supervised Machine Learning classifier (`scikit-learn` Pipeline with `StandardScaler` + `RandomForestClassifier`, 97.67% accuracy) assessing patient disease risk severity (Low, Moderate, High) with calibrated probability estimation.

---

## 🚀 Key Features

* **📱 Cross-Platform Mobile UI (Flet / Flutter Engine):** Modern Material 3 mobile navigation (Home, Scanner, Insights, ML Risk, History) with desktop mobile simulator and Android APK packaging.
* **🔍 OCR & Biomarker Parsing Engine:** Ingests medical report text/scans, automatically matches clinical tests against standard physiological reference ranges (e.g. FBS 70-100 mg/dL, HbA1c 4.0-5.6%, BP 120/80 mmHg), and tags markers as `NORMAL`, `HIGH`, or `LOW`.
* **🤖 GenAI Clinical Explainer (Hinglish):**
  - Instant triage level (`Normal`, `Moderate Caution`, `High Priority`).
  - Actionable dietary guidance (*"Meethi cheezein aur refined carbs kam karein"*).
  - Physical & lifestyle routine recommendations.
  - Medical consultation advisory.
* **🩺 Sanjeevani Risk Triage (ML Engine):**
  - Accepts 7 physiological biomarkers (Age, Blood Sugar, Systolic BP, Diastolic BP, BMI, Total Cholesterol, HbA1c).
  - Predicts real-time risk severity with visual progress gauge and probability distribution.
* **💾 Local SQLite Database:** Persistent history of past medical reports, risk assessments, and structured audit logs.
* **📊 Dual-Tier Logging & Observability:**
  - **Rotating File Logs:** `logs/app.log` (5MB rotating with backups) & `logs/error.log`.
  - **Database Audit Logs:** Structured `audit_logs` table tracking requests, OCR events, ML predictions, and chat queries with millisecond execution latency.
  - **In-App Logs Viewer & API:** `GET /api/logs` and interactive in-app dashboard.
* **⚡ FastAPI Microservice:** Low-latency REST endpoints with automatic OpenAPI documentation.

---

## 📂 Architecture & Directory Structure

```
MedScan AI/
├── app/                        # Mobile Android Application (Python / Flet)
│   ├── main.py                 # App entry point, AppBar & NavigationBar
│   ├── state.py                # State manager & FastAPI client
│   └── screens/
│       ├── home_screen.py      # Dashboard & quick actions
│       ├── scan_screen.py      # Camera / OCR scanner & demo presets
│       ├── report_screen.py    # GenAI clinical insights & biomarker cards
│       ├── risk_screen.py      # Sanjeevani ML risk calculator
│       └── history_screen.py   # Historical scan logs
│
├── backend/                    # AI & ML Backend Microservice (FastAPI)
│   ├── main.py                 # FastAPI endpoints (/api/scan, /api/explain, /api/predict-risk)
│   ├── ocr_engine.py           # OCR text extraction & clinical biomarker parser
│   ├── ai_explainer.py         # Groq LLM + Local Clinical NLP fallback
│   ├── database.py             # SQLite database operations
│   └── ml/
│       ├── train_model.py      # Scikit-learn training pipeline (97.67% accuracy)
│       └── diagnostic_model.joblib # Serialized model artifact
│
├── sample_data/                # Realistic test reports (Diabetes, CBC, Anemia)
├── requirements.txt            # Python dependencies
├── run_backend.py              # Script to start FastAPI server
├── run_app.py                  # Script to launch Mobile UI
├── run_all.py                  # Single-command launcher for both
├── test_backend.py             # Automated test suite
└── build_apk_guide.md          # Guide to generate Android .apk
```

---

## 🛠️ Quick Start Guide

### 1. Start the Backend Server:
```bash
python3 run_backend.py
```
*API will run at `http://127.0.0.1:8000` (Docs at `http://127.0.0.1:8000/docs`).*

### 2. Launch the Mobile Android UI:
```bash
python3 run_app.py
```
*(To open in web browser mobile simulator mode: `python3 run_app.py --web`)*

### 3. Or Launch Everything Concurrently:
```bash
python3 run_all.py
```

### 4. Run Automated Tests:
```bash
python3 test_backend.py
```

---

## 📱 Generating Android `.apk`
Refer to [build_apk_guide.md](build_apk_guide.md) for step-by-step instructions on generating release `.apk` files using Flet CLI or GitHub Actions in the cloud.

---

## 👨‍💻 Author & Credits
* **Developer:** Vikash Kumawat
* **Focus:** Generative AI, Machine Learning, Backend Engineering, Cross-Platform Mobile Apps
