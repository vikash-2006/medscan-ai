import flet as ft
from datetime import datetime
from app.state import state
from app.utils import show_snackbar

def build_report_screen(page: ft.Page, navigate_to) -> ft.Control:
    scan_data = state.current_scan_data
    explanation = state.current_explanation

    if not scan_data or not explanation:
        return ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED, size=64, color=ft.Colors.GREY_400),
                ft.Text("No Report Analyzed Yet", size=18, weight=ft.FontWeight.BOLD),
                ft.Text("Scan a lab report or select a preset in the Scanner tab to view AI clinical insights.",
                        size=13, color=ft.Colors.GREY_600, text_align=ft.TextAlign.CENTER),
                ft.Container(height=12),
                ft.FilledButton("Go to Scanner", icon=ft.Icons.DOCUMENT_SCANNER_ROUNDED, on_click=lambda _: navigate_to("scan_lab"))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment.CENTER,
            padding=32
        )

    urgency = explanation.get("urgency_level", "Normal")
    urgency_color = ft.Colors.GREEN_600
    urgency_bg = ft.Colors.GREEN_50
    if urgency == "High Priority":
        urgency_color = ft.Colors.RED_600
        urgency_bg = ft.Colors.RED_50
    elif urgency == "Moderate Caution":
        urgency_color = ft.Colors.AMBER_700
        urgency_bg = ft.Colors.AMBER_50

    urgency_badge = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SHIELD_OUTLINED, color=urgency_color, size=18),
            ft.Text(f"Triage Status: {urgency}", size=13, weight=ft.FontWeight.BOLD, color=urgency_color)
        ], spacing=6),
        padding=ft.Padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
        bgcolor=urgency_bg,
        border=ft.Border.all(1, urgency_color)
    )

    summary_card = ft.Card(
        elevation=1,
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.PSYCHOLOGY_ROUNDED, color=ft.Colors.TEAL_800),
                    ft.Text("AI Clinical Explanation (Hinglish)", size=14, weight=ft.FontWeight.BOLD),
                ], spacing=6),
                ft.Text(explanation.get("summary", ""), size=13, color=ft.Colors.GREY_800),
            ], spacing=8),
            padding=14,
            border_radius=12,
            bgcolor=ft.Colors.TEAL_50
        )
    )

    # Biomarkers chips/cards
    biomarkers = scan_data.get("biomarkers", [])
    marker_controls = []
    for b in biomarkers:
        st = b.get("status", "NORMAL")
        val_color = ft.Colors.GREEN_700 if st == "NORMAL" else (ft.Colors.RED_700 if st == "HIGH" else ft.Colors.AMBER_700)
        badge_bg = ft.Colors.GREEN_50 if st == "NORMAL" else (ft.Colors.RED_50 if st == "HIGH" else ft.Colors.AMBER_50)
        
        marker_controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Column([
                        ft.Text(b["name"], size=13, weight=ft.FontWeight.BOLD),
                        ft.Text(f"Ref Range: {b['reference_range']}", size=11, color=ft.Colors.GREY_600),
                    ], expand=True),
                    ft.Container(
                        content=ft.Column([
                            ft.Text(f"{b['value']} {b['unit']}", size=13, weight=ft.FontWeight.BOLD, color=val_color),
                            ft.Text(st, size=10, weight=ft.FontWeight.BOLD, color=val_color),
                        ], horizontal_alignment=ft.CrossAxisAlignment.END),
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        border_radius=8,
                        bgcolor=badge_bg
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.Padding.symmetric(vertical=6, horizontal=8),
                border=ft.Border.only(bottom=ft.BorderSide(0.5, ft.Colors.GREY_300))
            )
        )

    biomarker_card = ft.Card(
        elevation=1,
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.ANALYTICS_OUTLINED, color=ft.Colors.TEAL_700),
                    ft.Text(f"Extracted Biomarkers ({len(biomarkers)})", size=14, weight=ft.FontWeight.BOLD),
                ], spacing=6),
                ft.Column(marker_controls)
            ], spacing=8),
            padding=14,
            border_radius=12
        )
    )

    # Recommendations
    diet_items = [ft.Row([ft.Icon(ft.Icons.CHECK, size=14, color=ft.Colors.GREEN_600), ft.Text(d, size=12, expand=True)], spacing=6)
                  for d in explanation.get("diet_recommendations", [])]
    
    lifestyle_items = [ft.Row([ft.Icon(ft.Icons.FITNESS_CENTER_ROUNDED, size=14, color=ft.Colors.BLUE_600), ft.Text(l, size=12, expand=True)], spacing=6)
                       for l in explanation.get("lifestyle_tips", [])]

    advice_card = ft.Card(
        elevation=1,
        content=ft.Container(
            content=ft.Column([
                ft.Text("Dietary Guidance (Khaane-Peene ki Salah):", size=13, weight=ft.FontWeight.BOLD),
                *diet_items,
                ft.Divider(height=10),
                ft.Text("Lifestyle & Physical Routine:", size=13, weight=ft.FontWeight.BOLD),
                *lifestyle_items,
            ], spacing=6),
            padding=14,
            border_radius=12
        )
    )

    advisory_banner = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.INFO_ROUNDED, color=ft.Colors.BLUE_GREY_700, size=20),
            ft.Text(
                f"Doctor Advisory: {explanation.get('doctor_advisory', 'Consult physician for prescription.')}",
                size=12,
                color=ft.Colors.BLUE_GREY_900,
                expand=True
            )
        ], spacing=8),
        padding=12,
        border_radius=10,
        bgcolor=ft.Colors.BLUE_GREY_50
    )

    transfer_btn = ft.FilledButton(
        content=ft.Row([
            ft.Icon(ft.Icons.HEALTH_AND_SAFETY_ROUNDED),
            ft.Text("Transfer Vitals to Sanjeevani Risk Predictor", weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO_700,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=48,
        on_click=lambda _: navigate_to("risk_ml")
    )

    try:
        from fpdf import FPDF
        _FPDF_AVAILABLE = True
    except Exception:
        FPDF = None
        _FPDF_AVAILABLE = False
    
    import threading

    def _clean_pdf_text(text: str) -> str:
        if not text:
            return ""
        replacements = {
            "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
            "•": "*", "…": "...", "₹": "Rs. ", "✓": "[OK]", "⚠️": "[Caution]",
            "✅": "[Normal]", "❌": "[Alert]", "🔬": "", "🤖": "", "📄": "",
            "💊": "", "📊": "", "👋": "", "🩺": ""
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        return text.encode("latin-1", "replace").decode("latin-1")

    pdf_status = ft.Text("", size=11, color="#64748B")
    pdf_loading = ft.ProgressRing(width=16, height=16, stroke_width=2, visible=False)
    
    def download_pdf(e):
        if not _FPDF_AVAILABLE or FPDF is None:
            show_snackbar(page, "PDF export library not available.", bgcolor="#DC2626")
            return

        pdf_loading.visible = True
        pdf_status.value = "📄 Generating PDF report..."
        page.update()

        def _generate():
            try:
                pdf = FPDF()
                pdf.add_page()
                pdf.set_auto_page_break(auto=True, margin=15)
                
                # Header
                pdf.set_font("Arial", 'B', 16)
                pdf.cell(0, 10, txt=_clean_pdf_text(state.current_report_title), ln=True, align='C')
                
                pdf.set_font("Arial", size=10)
                date_str = datetime.now().strftime("%d %b %Y, %I:%M %p")
                patient = getattr(state, "patient_name", "Patient")
                pdf.cell(0, 6, txt=_clean_pdf_text(f"Patient: {patient}  |  Generated: {date_str}"), ln=True, align='C')
                pdf.ln(4)
                
                # Urgency Status
                pdf.set_font("Arial", 'B', 11)
                pdf.cell(0, 8, txt=_clean_pdf_text(f"Triage Level: {urgency}"), ln=True)
                pdf.ln(2)
                
                # Clinical Summary
                pdf.set_font("Arial", 'B', 12)
                pdf.cell(0, 8, txt="Clinical Interpretation Summary:", ln=True)
                pdf.set_font("Arial", size=10)
                pdf.multi_cell(0, 6, txt=_clean_pdf_text(explanation.get("summary", "No summary available.")))
                pdf.ln(4)
                
                # Biomarkers Table
                biomarkers = scan_data.get("biomarkers", [])
                if biomarkers:
                    pdf.set_font("Arial", 'B', 11)
                    pdf.cell(0, 8, txt="Biomarkers Detected:", ln=True)
                    pdf.set_font("Arial", 'B', 9)
                    pdf.cell(60, 7, txt="Biomarker", border=1)
                    pdf.cell(35, 7, txt="Value", border=1)
                    pdf.cell(30, 7, txt="Status", border=1)
                    pdf.cell(60, 7, txt="Reference Range", border=1, ln=True)
                    
                    pdf.set_font("Arial", size=9)
                    for b in biomarkers:
                        name = _clean_pdf_text(str(b.get("name", "")))[:28]
                        val = _clean_pdf_text(f"{b.get('value', '')} {b.get('unit', '')}")
                        st = _clean_pdf_text(str(b.get("status", "NORMAL")))
                        ref = _clean_pdf_text(str(b.get("reference_range", "")))
                        pdf.cell(60, 6, txt=name, border=1)
                        pdf.cell(35, 6, txt=val, border=1)
                        pdf.cell(30, 6, txt=st, border=1)
                        pdf.cell(60, 6, txt=ref, border=1, ln=True)
                    pdf.ln(4)

                # Diet & Lifestyle Recommendations
                diet_tips = explanation.get("diet_recommendations", [])
                if diet_tips:
                    pdf.set_font("Arial", 'B', 11)
                    pdf.cell(0, 8, txt="Dietary Recommendations:", ln=True)
                    pdf.set_font("Arial", size=10)
                    for tip in diet_tips:
                        pdf.multi_cell(0, 5, txt=_clean_pdf_text(f"- {tip}"))
                    pdf.ln(3)

                # Doctor Advisory
                advisory = explanation.get("doctor_advisory", "")
                if advisory:
                    pdf.set_font("Arial", 'B', 11)
                    pdf.cell(0, 8, txt="Medical Advisory:", ln=True)
                    pdf.set_font("Arial", 'I', 10)
                    pdf.multi_cell(0, 5, txt=_clean_pdf_text(advisory))
                    pdf.ln(4)

                filename = f"report_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
                pdf.output(filename)
                pdf_loading.visible = False
                pdf_status.value = f"Saved: {filename}"
                show_snackbar(page, f"PDF report saved: {filename}", bgcolor="#16A34A")
                page.update()
            except Exception as ex:
                pdf_loading.visible = False
                pdf_status.value = f"Export error: {str(ex)}"
                show_snackbar(page, f"PDF export failed: {str(ex)}", bgcolor="#DC2626")
                page.update()
        
        threading.Thread(target=_generate, daemon=True).start()

    consult_btn = ft.FilledButton(
        content=ft.Row([
            ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED),
            ft.Text("Consult a Doctor for These Findings", weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        style=ft.ButtonStyle(
            bgcolor="#2563EB",
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=48,
        on_click=lambda _: navigate_to("doctors")
    )
    
    pdf_btn = ft.OutlinedButton(
        content=ft.Row([
            ft.Icon(ft.Icons.PICTURE_AS_PDF_ROUNDED),
            ft.Text("Download PDF Report", weight=ft.FontWeight.BOLD),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        height=48,
        on_click=download_pdf
    )

    return ft.ListView(
        controls=[
            ft.Row([
                ft.Text(state.current_report_title, size=18, weight=ft.FontWeight.BOLD, expand=True),
                urgency_badge
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=4),
            summary_card,
            ft.Container(height=4),
            biomarker_card,
            ft.Container(height=4),
            advice_card,
            ft.Container(height=4),
            advisory_banner,
            ft.Container(height=10),
            transfer_btn,
            ft.Container(height=6),
            consult_btn,
            ft.Container(height=6),
            pdf_btn,
            ft.Row([pdf_loading, pdf_status], spacing=6),
            ft.Container(height=25)
        ],
        spacing=8,
        padding=16
    )
