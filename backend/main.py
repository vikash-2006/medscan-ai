import os
import time
import shutil
import tempfile
import joblib
import numpy as np

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
from typing import Dict, Any, Optional, List
from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from .ocr_engine import OCREngine
from .ai_explainer import AIExplainer
from .logger import logger, APP_LOG_FILE
from .database import (
    init_db, save_report, get_reports, 
    save_risk_assessment, get_risk_assessments,
    insert_log, get_audit_logs,
    save_appointment, get_appointments, cancel_appointment
)

app = FastAPI(title="MedScan AI & Sanjeevani Diagnostic API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Automated HTTP Request & Latency Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    client_ip = request.client.host if request.client else "127.0.0.1"
    
    response = await call_next(request)
    duration_ms = round((time.time() - start_time) * 1000, 2)
    path = request.url.path

    # Filter out high-frequency static asset hits from database to prevent clutter
    if not path.startswith("/assets") and not path.startswith("/static"):
        log_msg = f"{request.method} {path} - Status: {response.status_code} - {duration_ms}ms - IP: {client_ip}"
        if response.status_code >= 400:
            logger.warning(log_msg)
        else:
            logger.info(log_msg)

        try:
            insert_log(
                level="INFO" if response.status_code < 400 else "WARN",
                category="API_REQUEST",
                action=f"{request.method} {path}",
                details={"status_code": response.status_code, "duration_ms": duration_ms},
                ip_address=client_ip
            )
        except Exception as e:
            logger.error(f"Failed to record audit log: {e}")

    return response

# Initialize subsystems
init_db()
ocr = OCREngine()
explainer = AIExplainer()

# Load Sanjeevani ML Diagnostic Pipeline
MODEL_PATH = os.path.join(os.path.dirname(__file__), "ml", "diagnostic_model.joblib")
model_artifact = None

def get_model():
    global model_artifact
    if model_artifact is None and os.path.exists(MODEL_PATH):
        try:
            model_artifact = joblib.load(MODEL_PATH)
            print("Successfully loaded Sanjeevani ML Diagnostic Pipeline.")
        except Exception as e:
            print(f"[Model Warning] Could not load model: {e}")
    return model_artifact

class VitalsRequest(BaseModel):
    patient_name: Optional[str] = "Patient"
    age: float = 45.0
    blood_sugar: float = 110.0
    blood_pressure_sys: float = 125.0
    blood_pressure_dia: float = 80.0
    bmi: float = 24.5
    cholesterol: float = 190.0
    hba1c: float = 5.6

class ExplainRequest(BaseModel):
    title: Optional[str] = "Medical Report"
    raw_text: Optional[str] = ""
    biomarkers: List[Dict[str, Any]]
    language: Optional[str] = "hinglish"
    save_to_history: Optional[bool] = True

@app.get("/api/health")
def health():
    return {"status": "online", "service": "MedScan AI & Sanjeevani Diagnostic Backend"}

@app.post("/api/scan")
async def scan_medical_report(file: UploadFile = File(None), raw_text: Optional[str] = Form(None)):
    """
    Accepts uploaded report image (JPEG/PNG) or raw clinical text.
    Extracts text using OCR and parses structured biomarkers.
    """
    extracted_text = ""
    source_type = "file_upload" if file else "raw_text"
    logger.info(f"Incoming report scan request via {source_type} (Filename: {file.filename if file else 'None'})")

    if file:
        tmp_path = None
        try:
            suffix = os.path.splitext(file.filename or "")[1] or ".png"
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                shutil.copyfileobj(file.file, tmp)
                tmp_path = tmp.name
            extracted_text = ocr.extract_text(tmp_path)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error processing uploaded file: {e}")
            raise HTTPException(status_code=500, detail=f"File processing error: {str(e)}")
        finally:
            if tmp_path and os.path.exists(tmp_path):
                try:
                    os.remove(tmp_path)
                except Exception:
                    pass
    elif raw_text:
        extracted_text = raw_text
    else:
        logger.warning("Scan request rejected: Neither file nor raw_text provided.")
        raise HTTPException(status_code=400, detail="Either file or raw_text must be provided")

    parsed = ocr.parse_biomarkers(extracted_text)
    
    # Store Audit Log
    logger.info(f"OCR Scan completed: Extracted {parsed['markers_count']} markers ({parsed['abnormal_count']} abnormal)")
    insert_log(
        level="INFO",
        category="OCR_SCAN",
        action="Scanned medical report",
        details={
            "source": source_type,
            "filename": file.filename if file else None,
            "markers_count": parsed["markers_count"],
            "abnormal_count": parsed["abnormal_count"],
            "detected_biomarkers": [m["name"] for m in parsed["biomarkers"]]
        }
    )

    return {
        "status": "success",
        "raw_text": extracted_text,
        "biomarkers": parsed["biomarkers"],
        "raw_values": parsed["raw_values"],
        "markers_count": parsed["markers_count"],
        "abnormal_count": parsed["abnormal_count"]
    }

@app.post("/api/explain")
def explain_report(req: ExplainRequest):
    """
    Interprets extracted biomarkers using Generative AI (Groq / Clinical NLP Engine).
    """
    logger.info(f"Generating AI clinical explanation for '{req.title}' ({len(req.biomarkers)} markers)")
    explanation = explainer.generate_explanation(
        {"biomarkers": req.biomarkers},
        language=req.language or "hinglish"
    )
    
    saved_id = None
    if req.save_to_history:
        saved_id = save_report(
            title=req.title or "Medical Report",
            raw_text=req.raw_text or "",
            biomarkers=req.biomarkers,
            explanation=explanation
        )

    # Store Audit Log
    insert_log(
        level="INFO",
        category="AI_EXPLAIN",
        action=f"Explained report: {req.title}",
        details={
            "report_id": saved_id,
            "urgency_level": explanation.get("urgency_level"),
            "language": req.language or "hinglish",
            "findings_count": len(explanation.get("key_findings", []))
        }
    )

    return {
        "status": "success",
        "report_id": saved_id,
        "explanation": explanation
    }

@app.post("/api/predict-risk")
def predict_health_risk(vitals: VitalsRequest):
    """
    Runs the Sanjeevani ML Classifier on patient health metrics.
    Predicts disease risk level (Low, Moderate, High) with confidence probabilities.
    """
    artifact = get_model()
    if not artifact:
        logger.error("Diagnostic ML Model artifact could not be loaded from disk.")
        raise HTTPException(status_code=500, detail="Diagnostic ML Model not available on server")

    pipeline = artifact["pipeline"]
    classes = artifact["classes"]

    vector = np.array([[
        vitals.age,
        vitals.blood_sugar,
        vitals.blood_pressure_sys,
        vitals.blood_pressure_dia,
        vitals.bmi,
        vitals.cholesterol,
        vitals.hba1c
    ]])

    pred_class_idx = int(pipeline.predict(vector)[0])
    predicted_label = classes[pred_class_idx]

    probs = pipeline.predict_proba(vector)[0]
    confidence = float(probs[pred_class_idx]) * 100.0

    color_map = {
        "Low Risk": "#10B981",
        "Moderate Risk": "#F59E0B",
        "High Risk": "#EF4444"
    }
    
    advice_map = {
        "Low Risk": "Health parameters are stable. Continue regular physical activity and balanced diet.",
        "Moderate Risk": "Borderline risk detected. Lifestyle intervention, salt/sugar control, and 3-month follow-up recommended.",
        "High Risk": "High clinical risk detected. Consultation with a medical practitioner is strongly advised."
    }

    assessment_id = save_risk_assessment(
        patient_name=vitals.patient_name,
        vitals=vitals.model_dump(),
        risk=predicted_label,
        prob=confidence
    )

    # Store Audit Log
    logger.info(f"ML Diagnostic prediction for '{vitals.patient_name}': {predicted_label} ({round(confidence, 1)}%)")
    insert_log(
        level="WARN" if predicted_label == "High Risk" else "INFO",
        category="ML_INFERENCE",
        action="Assessed disease risk",
        details={
            "assessment_id": assessment_id,
            "patient_name": vitals.patient_name,
            "predicted_risk": predicted_label,
            "confidence": round(confidence, 1),
            "vitals": vitals.model_dump()
        }
    )

    return {
        "assessment_id": assessment_id,
        "predicted_risk": predicted_label,
        "confidence": round(confidence, 1),
        "risk_color": color_map.get(predicted_label, "#3B82F6"),
        "probabilities": {classes[i]: round(float(probs[i]) * 100.0, 1) for i in range(len(classes))},
        "clinical_advice": advice_map.get(predicted_label, "")
    }

class ChatMessageRequest(BaseModel):
    message: str
    patient_name: Optional[str] = "Vikash"

@app.post("/api/chat")
def handle_chat_query(req: ChatMessageRequest):
    """
    Handles conversational questions, generates medical guidance, and records chat logs.
    """
    logger.info(f"Conversational query from '{req.patient_name}': {req.message}")
    
    text_lower = req.message.lower()
    if "pain" in text_lower or "stomach" in text_lower:
        reply = "Stomach pain acidity, indigestion ya infection ki wajah se ho sakta hai. Halka khana lein aur hydrate rahein. Agar dard tej ho toh doctor se consult karein."
    elif "sugar" in text_lower or "diabetes" in text_lower:
        reply = "Fasting blood sugar 70-100 mg/dL normal hota hai. 126 mg/dL se upar diabetes indicate karta hai. Aap 'Health Reports' me lab report upload kar sakte hain."
    elif "bp" in text_lower or "pressure" in text_lower:
        reply = "Standard blood pressure 120/80 mmHg hota hai. 140/90 se upar hypertension mana jata hai. Sodium intake kam karein."
    else:
        reply = "Main aapke symptoms samajh gaya hoon. Iske detailed analysis ke liye 'Check Symptoms' par click karke apna risk score calculate karein."

    insert_log(
        level="INFO",
        category="CHAT",
        action="Processed AI conversational message",
        details={"patient": req.patient_name, "query": req.message, "reply": reply}
    )

    return {"status": "success", "reply": reply}

class ClientLogRequest(BaseModel):
    category: str
    action: str
    details: Optional[Dict[str, Any]] = None
    level: Optional[str] = "INFO"

@app.post("/api/logs/client")
def record_client_log(req: ClientLogRequest):
    """
    Receives frontend user interaction logs (button clicks, voice sessions, tab changes).
    """
    insert_log(
        level=req.level or "INFO",
        category=req.category,
        action=req.action,
        details=req.details
    )
    logger.info(f"[CLIENT LOG] [{req.category}] {req.action}")
    return {"status": "logged"}

@app.get("/api/logs")
def get_system_logs(limit: int = 50, category: Optional[str] = None, level: Optional[str] = None):
    """
    Retrieves both structured database audit logs and raw file logs for observability.
    """
    db_logs = get_audit_logs(limit=limit, category=category, level=level)
    
    file_tail = []
    if os.path.exists(APP_LOG_FILE):
        try:
            with open(APP_LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                file_tail = [l.strip() for l in lines[-limit:]]
        except Exception as e:
            file_tail = [f"Error reading log file: {e}"]

    return {
        "status": "success",
        "total_database_logs": len(db_logs),
        "audit_logs": db_logs,
        "log_file_path": APP_LOG_FILE,
        "file_log_tail": file_tail
    }

@app.get("/api/history")
def get_scan_history(limit: int = 15):
    reports = get_reports(limit=limit)
    risk_checks = get_risk_assessments(limit=limit)
    return {
        "reports": reports,
        "risk_assessments": risk_checks
    }

class AppointmentBookingRequest(BaseModel):
    patient_name: Optional[str] = "Vikash Kumawat"
    doctor_name: str
    specialty: str
    date_str: str
    time_str: str
    fee: Optional[str] = "₹500"
    avatar: Optional[str] = "doctor_portrait.jpg"
    status: Optional[str] = "Confirmed"

@app.post("/api/appointments")
def create_appointment(req: AppointmentBookingRequest):
    appt_id = save_appointment(
        patient_name=req.patient_name,
        doctor_name=req.doctor_name,
        specialty=req.specialty,
        date_str=req.date_str,
        time_str=req.time_str,
        fee=req.fee or "₹500",
        avatar=req.avatar or "doctor_portrait.jpg",
        status=req.status or "Confirmed"
    )
    insert_log(
        level="INFO",
        category="APPOINTMENT",
        action="Booked doctor consultation",
        details={"appointment_id": appt_id, "doctor": req.doctor_name, "date": req.date_str, "time": req.time_str}
    )
    return {
        "status": "success",
        "appointment_id": appt_id,
        "message": f"Appointment booked with {req.doctor_name} for {req.date_str} at {req.time_str}"
    }

@app.get("/api/appointments")
def list_appointments(limit: int = 50):
    return {
        "status": "success",
        "appointments": get_appointments(limit=limit)
    }

@app.delete("/api/appointments/{appointment_id}")
def remove_appointment(appointment_id: int):
    success = cancel_appointment(appointment_id)
    return {"status": "success" if success else "not_found", "cancelled": success}

# Mount and serve modern interactive Web Frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dir, "assets")), name="assets")

@app.get("/")
def serve_frontend_ui():
    index_path = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"status": "online", "service": "AURA Medical & MedScan AI"}

