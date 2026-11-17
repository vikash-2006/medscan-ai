import os
import re
import json
from typing import Dict, Any, List

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

class AIExplainer:
    def __init__(self, api_key: str = None):
        self.groq_api_key = api_key or os.getenv("GROQ_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.openai_api_key = os.getenv("OPENAI_API_KEY")

        self.groq_client = None
        self.gemini_client = None
        self.openai_client = None

        # 1. Initialize Groq
        if self.groq_api_key:
            try:
                from groq import Groq
                self.groq_client = Groq(api_key=self.groq_api_key)
            except Exception as e:
                print(f"[Warning] Groq client initialization failed: {e}")

        # 2. Initialize Google Gemini
        if self.gemini_api_key:
            try:
                import google.generativeai as genai
                genai.configure(api_key=self.gemini_api_key)
                self.gemini_client = genai
            except Exception as e:
                print(f"[Warning] Gemini client initialization failed: {e}")

        # 3. Initialize OpenAI
        if self.openai_api_key:
            try:
                from openai import OpenAI
                self.openai_client = OpenAI(api_key=self.openai_api_key)
            except Exception as e:
                print(f"[Warning] OpenAI client initialization failed: {e}")

    def generate_explanation(self, parsed_data: Dict[str, Any], language: str = "hinglish") -> Dict[str, Any]:
        """
        Generates clinical interpretation for extracted medical biomarkers.
        Cascade: Groq (ultra-fast 120B/20B) -> Gemini -> OpenAI -> Local Clinical NLP Engine.
        """
        biomarkers = parsed_data.get("biomarkers", [])
        if not biomarkers:
            return self._local_clinical_explanation(biomarkers, language)

        # 1. Try Groq Cloud
        if self.groq_client:
            try:
                return self._call_groq_llm(biomarkers, language)
            except Exception as e:
                print(f"[LLM Warning] Groq call failed: {e}. Trying secondary providers...")

        # 2. Try Google Gemini
        if self.gemini_client:
            try:
                return self._call_gemini_llm(biomarkers, language)
            except Exception as e:
                print(f"[LLM Warning] Gemini call failed: {e}. Trying fallback...")

        # 3. Try OpenAI
        if self.openai_client:
            try:
                return self._call_openai_llm(biomarkers, language)
            except Exception as e:
                print(f"[LLM Warning] OpenAI call failed: {e}...")

        # 4. Resilient Local Deterministic Clinical Engine
        return self._local_clinical_explanation(biomarkers, language)

    def _clean_json_response(self, text: str) -> Dict[str, Any]:
        """Strips markdown code fences and parses valid JSON."""
        cleaned = text.strip()
        if "```json" in cleaned:
            cleaned = cleaned.split("```json", 1)[1]
            if "```" in cleaned:
                cleaned = cleaned.split("```", 1)[0]
        elif "```" in cleaned:
            cleaned = cleaned.split("```", 1)[1]
            if "```" in cleaned:
                cleaned = cleaned.split("```", 1)[0]
        cleaned = cleaned.strip()
        return json.loads(cleaned)

    def _call_groq_llm(self, biomarkers: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        prompt = f"""You are MedScan AI, an empathetic and professional medical clinical assistant.
Given these lab test results:
{json.dumps(biomarkers, indent=2)}

Provide a clear, patient-friendly report interpretation in {language.upper()}.
Return ONLY a valid JSON object with the following exact keys:
- "summary": A brief 2-line empathetic summary of overall health based on these findings.
- "key_findings": List of strings describing each biomarker status (which is normal, which is high/low).
- "diet_recommendations": List of 3-4 actionable dietary tips.
- "lifestyle_tips": List of 2-3 lifestyle habits (exercise, sleep, hydration).
- "urgency_level": "Normal", "Moderate Caution", or "High Priority".
- "doctor_advisory": Recommendation on whether and when to consult a doctor.
"""
        models_to_try = [
            "openai/gpt-oss-120b",
            "openai/gpt-oss-20b",
            "qwen/qwen3.8-27b",
            "llama-3.3-70b-versatile",
            "llama-3.1-70b-versatile"
        ]
        for model in models_to_try:
            try:
                response = self.groq_client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a helpful clinical report interpreter. Always respond in valid JSON format only."},
                        {"role": "user", "content": prompt}
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.3
                )
                content = response.choices[0].message.content
                return self._clean_json_response(content)
            except Exception:
                continue
        raise RuntimeError("All Groq model attempts failed")

    def _call_gemini_llm(self, biomarkers: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        prompt = f"""You are MedScan AI, an empathetic and professional medical assistant.
Given these lab test results:
{json.dumps(biomarkers, indent=2)}

Provide a patient-friendly report interpretation in {language.upper()}.
Return ONLY a valid JSON object with these keys:
"summary", "key_findings", "diet_recommendations", "lifestyle_tips", "urgency_level", "doctor_advisory".
"""
        for m_name in ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]:
            try:
                model = self.gemini_client.GenerativeModel(m_name)
                resp = model.generate_content(prompt)
                return self._clean_json_response(resp.text)
            except Exception:
                continue
        raise RuntimeError("All Gemini model attempts failed")

    def _call_openai_llm(self, biomarkers: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        prompt = f"""You are MedScan AI, an empathetic and professional medical assistant.
Given these lab test results:
{json.dumps(biomarkers, indent=2)}

Provide a clear, patient-friendly report interpretation in {language.upper()}.
Return ONLY a valid JSON object with keys:
"summary", "key_findings", "diet_recommendations", "lifestyle_tips", "urgency_level", "doctor_advisory".
"""
        resp = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a clinical report interpreter. Respond in valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        return self._clean_json_response(resp.choices[0].message.content)

    def _local_clinical_explanation(self, biomarkers: List[Dict[str, Any]], language: str) -> Dict[str, Any]:
        """
        Deterministic, rule-based clinical intelligence engine.
        Outputs rich structured insight even without internet or API key.
        """
        abnormals = [b for b in biomarkers if b.get("status") != "NORMAL"]
        normals = [b for b in biomarkers if b.get("status") == "NORMAL"]
        
        urgency = "Normal"
        if len(abnormals) >= 3:
            urgency = "High Priority"
        elif len(abnormals) >= 1:
            urgency = "Moderate Caution"

        key_findings = []
        diet_tips = []
        lifestyle_tips = []

        # Analyze individual markers
        for b in biomarkers:
            name = b["name"]
            val = b["value"]
            unit = b["unit"]
            status = b["status"]
            ref = b["reference_range"]

            if status == "HIGH":
                if "sugar" in name.lower() or "glucose" in name.lower() or "hba1c" in name.lower():
                    key_findings.append(f"⚠️ {name}: {val} {unit} (High) — Sugar levels elevated hain (Normal range: {ref}).")
                    diet_tips.append("Meethi cheezein, cold drinks aur refined carbohydrates (maida, white rice) kam karein.")
                    diet_tips.append("Khane me fiber badhayein: hari sabziya, oats, aur methi dana shamil karein.")
                    lifestyle_tips.append("Daily 30 minutes brisk walk ya light exercise karein.")
                elif "pressure" in name.lower():
                    key_findings.append(f"⚠️ {name}: {val} {unit} (High) — Blood pressure normal se zyada note hua hai.")
                    diet_tips.append("Namak (sodium) ka sevan kam karein aur packaged/junk food avoid karein.")
                    lifestyle_tips.append("Stress kam karne ke liye pranayama ya meditation karein aur proper 7-8 ghante ki neend lein.")
                elif "cholesterol" in name.lower():
                    key_findings.append(f"⚠️ {name}: {val} {unit} (High) — Lipid profile me cholesterol high hai.")
                    diet_tips.append("Tali-bhuni (fried) cheezein aur excess ghee/butter kam karein.")
                else:
                    key_findings.append(f"⚠️ {name}: {val} {unit} (High) — Normal range ({ref}) se upar hai.")
            elif status == "LOW":
                if "hemoglobin" in name.lower():
                    key_findings.append(f"⚠️ {name}: {val} {unit} (Low) — Anemia/low iron ka sign ho sakta hai.")
                    diet_tips.append("Iron-rich diet lein jaise palak, anar, chukandar (beetroot), aur dates.")
                elif "platelet" in name.lower():
                    key_findings.append(f"⚠️ {name}: {val} {unit} (Low) — Platelet count kam hai.")
                    diet_tips.append("Papaya leaf extract, kiwi, aur coconut water hydration ke liye lein.")
                else:
                    key_findings.append(f"⚠️ {name}: {val} {unit} (Low) — Normal range ({ref}) se kam hai.")
            else:
                key_findings.append(f"✅ {name}: {val} {unit} (Normal) — Normal parameters ke andar hai.")

        if not diet_tips:
            diet_tips = [
                "Balanced diet lein jisme green vegetables aur seasonal fruits hon.",
                "Pura din adequate paani (2.5-3 liters) piyein.",
                "Late-night heavy meals avoid karein."
            ]

        if not lifestyle_tips:
            lifestyle_tips = [
                "Regular daily 30-40 minutes physical activity ya walking karein.",
                "Quality sleep schedule (7-8 hours) maintain karein."
            ]

        if urgency == "High Priority":
            summary = "Aapki report me multiple biomarkers abnormal range me hain. Inhe control me laane ke liye doctor ka consultation zaroori hai."
            advisory = "Doctor se jaldi consult karein aur unke bataye anusaar prescription follow karein."
        elif urgency == "Moderate Caution":
            summary = "Kuch values borderline ya thodi elevated hain. Lifestyle aur diet changes se inme kafi sudhar ho sakta hai."
            advisory = "Apne physician ko ye report dikhayein aur 1-2 mahine me repeat test karwayein."
        else:
            summary = "Shandar! Aapke scan kiye gaye biomarkers standard normal range me hain. Healthy lifestyle continue rakhein."
            advisory = "Routine health checkup har 6 se 12 mahine me continue karein."

        return {
            "summary": summary,
            "key_findings": key_findings,
            "diet_recommendations": list(dict.fromkeys(diet_tips))[:4],
            "lifestyle_tips": list(dict.fromkeys(lifestyle_tips))[:3],
            "urgency_level": urgency,
            "doctor_advisory": advisory
        }
