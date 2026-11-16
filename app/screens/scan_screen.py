import flet as ft
from app.state import state

SAMPLE_REPORTS = {
    "Diabetes & Lipid (High Risk)": """METROPOLITAN DIAGNOSTIC LABS
Patient Name: Vikash Kumawat       Age: 52 Yrs
Referring Dr: Dr. Sharma, MD       Date: 2026-11-16
-------------------------------------------------------------
TEST NAME                        RESULT    UNIT       REFERENCE
-------------------------------------------------------------
Fasting Blood Sugar (FBS)        158.0     mg/dL      (70 - 100)
HbA1c (Glycated Hemoglobin)      7.6       %          (4.0 - 5.6)
Blood Pressure (Systolic/Dia)    148/94    mmHg       (120/80)
Total Cholesterol                245.0     mg/dL      (125 - 200)
Serum Creatinine                 1.1       mg/dL      (0.6 - 1.3)
Hemoglobin                       13.8      g/dL       (12.0 - 16.5)
-------------------------------------------------------------
Impression: Elevated glycemic parameters & Grade 1 Hypertension.""",

    "Normal CBC & Vitals (Healthy)": """APOLLO HEALTH PATHOLOGY
Patient Name: Vikash Kumawat       Age: 24 Yrs
Date: 2026-11-16
-------------------------------------------------------------
TEST NAME                        RESULT    UNIT       REFERENCE
-------------------------------------------------------------
Fasting Blood Sugar              88.0      mg/dL      (70 - 100)
HbA1c                            5.2       %          (4.0 - 5.6)
Blood Pressure                   118/78    mmHg       (120/80)
Total Cholesterol                165.0     mg/dL      (125 - 200)
Hemoglobin                       14.8      g/dL       (12.0 - 16.5)
Total WBC Count                  6800      /cumm      (4000 - 11000)
Platelet Count                   2.8       lakh/cumm  (1.5 - 4.5)
-------------------------------------------------------------
Impression: All biological parameters within normal physiological limits.""",

    "Low Hemoglobin (Anemia Profile)": """CITY CARE CLINIC
Patient Name: Sunita Sharma        Age: 38 Yrs
Date: 2026-11-16
-------------------------------------------------------------
TEST NAME                        RESULT    UNIT       REFERENCE
-------------------------------------------------------------
Hemoglobin (Hb)                  9.4       g/dL       (12.0 - 16.5)
Total WBC Count                  5200      /cumm      (4000 - 11000)
Platelet Count                   1.8       lakh/cumm  (1.5 - 4.5)
Blood Sugar Fasting              92.0      mg/dL      (70 - 100)
Blood Pressure                   115/75    mmHg       (120/80)
Total Cholesterol                180.0     mg/dL      (125 - 200)
-------------------------------------------------------------
Impression: Microcytic hypochromic profile; Moderate Iron deficiency suspected."""
}

def build_scan_screen(page: ft.Page, navigate_to) -> ft.Control:
    title_field = ft.TextField(
        label="Report Title / Patient Name",
        value="Medical Lab Report",
        prefix_icon=ft.Icons.BADGE_OUTLINED,
        dense=True
    )

    report_text_field = ft.TextField(
        label="Report OCR / Clinical Text",
        multiline=True,
        min_lines=6,
        max_lines=12,
        value=SAMPLE_REPORTS["Diabetes & Lipid (High Risk)"],
        hint_text="Paste medical report text or select a demo sample below...",
        text_size=12
    )

    loading_ring = ft.ProgressRing(visible=False, width=24, height=24, stroke_width=3)
    status_label = ft.Text("", size=12, color=ft.Colors.GREY_700)

    def load_preset(e, sample_key):
        report_text_field.value = SAMPLE_REPORTS[sample_key]
        title_field.value = f"Report: {sample_key}"
        page.update()

    def handle_analyze(e):
        txt = report_text_field.value.strip()
        if not txt:
            page.open(ft.SnackBar(ft.Text("Please enter or paste report text to analyze!")))
            return

        loading_ring.visible = True
        analyze_btn.disabled = True
        status_label.value = "Extracting biomarkers & running AI clinical analysis..."
        page.update()

        try:
            state.current_report_title = title_field.value
            # Step 1: Scan & Parse
            state.scan_medical_report(raw_text=txt)
            # Step 2: Explain with AI
            state.generate_ai_explanation(language="hinglish")
            
            loading_ring.visible = False
            analyze_btn.disabled = False
            status_label.value = "Analysis complete! Navigating to insights..."
            page.update()
            
            # Navigate to Report / Insights Tab (Index 2)
            navigate_to(2)
        except Exception as ex:
            loading_ring.visible = False
            analyze_btn.disabled = False
            status_label.value = f"Error: {str(ex)}"
            page.open(ft.SnackBar(ft.Text(f"Failed to analyze report: {str(ex)}")))
            page.update()

    analyze_btn = ft.FilledButton(
        content=ft.Row([
            ft.Icon(ft.Icons.AUTO_AWESOME_ROUNDED),
            ft.Text("Analyze Report with AI", weight=ft.FontWeight.BOLD),
            loading_ring
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.TEAL_700,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10),
        ),
        height=48,
        on_click=handle_analyze
    )

    preset_chips = ft.Row([
        ft.ActionChip(
            label=ft.Text("Sample 1: High Risk", size=11),
            avatar=ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, size=16, color=ft.Colors.RED_600),
            on_click=lambda e: load_preset(e, "Diabetes & Lipid (High Risk)")
        ),
        ft.ActionChip(
            label=ft.Text("Sample 2: Normal", size=11),
            avatar=ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED, size=16, color=ft.Colors.GREEN_600),
            on_click=lambda e: load_preset(e, "Normal CBC & Vitals (Healthy)")
        ),
        ft.ActionChip(
            label=ft.Text("Sample 3: Anemia", size=11),
            avatar=ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED, size=16, color=ft.Colors.AMBER_600),
            on_click=lambda e: load_preset(e, "Low Hemoglobin (Anemia Profile)")
        ),
    ], scroll=ft.ScrollMode.ADAPTIVE, spacing=8)

    return ft.ListView(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.DOCUMENT_SCANNER_ROUNDED, color=ft.Colors.TEAL_800),
                ft.Text("Smart Report Scanner", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=8),
            ft.Text("Upload prescription / lab test or select a pre-loaded sample report.", size=12, color=ft.Colors.GREY_600),
            ft.Container(height=8),
            title_field,
            ft.Container(height=6),
            ft.Text("Quick Demo Presets:", size=12, weight=ft.FontWeight.W_600, color=ft.Colors.GREY_700),
            preset_chips,
            ft.Container(height=6),
            report_text_field,
            ft.Container(height=10),
            analyze_btn,
            ft.Container(content=status_label, alignment=ft.alignment.center)
        ],
        spacing=8,
        padding=16
    )
