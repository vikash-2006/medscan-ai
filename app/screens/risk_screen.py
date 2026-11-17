import flet as ft
from app.state import state
from app.utils import show_snackbar

def build_risk_screen(page: ft.Page, navigate_to) -> ft.Control:
    vitals = state.current_vitals

    age_input = ft.TextField(
        label="Age (Years)",
        value=str(int(vitals.get("age", 45))),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    sugar_input = ft.TextField(
        label="Fasting Blood Sugar (mg/dL)",
        value=str(round(vitals.get("blood_sugar", 120), 1)),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    bp_sys_input = ft.TextField(
        label="Systolic BP (mmHg)",
        value=str(int(vitals.get("blood_pressure_sys", 130))),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    bp_dia_input = ft.TextField(
        label="Diastolic BP (mmHg)",
        value=str(int(vitals.get("blood_pressure_dia", 85))),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    bmi_input = ft.TextField(
        label="BMI (kg/m²)",
        value=str(round(vitals.get("bmi", 25.5), 1)),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    chol_input = ft.TextField(
        label="Total Cholesterol (mg/dL)",
        value=str(int(vitals.get("cholesterol", 210))),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    hba1c_input = ft.TextField(
        label="HbA1c (%)",
        value=str(round(vitals.get("hba1c", 6.0), 1)),
        keyboard_type=ft.KeyboardType.NUMBER,
        dense=True,
        expand=True
    )

    result_container = ft.Column(visible=False, spacing=8)
    loading_ring = ft.ProgressRing(visible=False, width=22, height=22, stroke_width=3)

    def run_prediction(e):
        try:
            loading_ring.visible = True
            predict_btn.disabled = True
            page.update()

            data = {
                "age": float(age_input.value or 45),
                "blood_sugar": float(sugar_input.value or 100),
                "blood_pressure_sys": float(bp_sys_input.value or 120),
                "blood_pressure_dia": float(bp_dia_input.value or 80),
                "bmi": float(bmi_input.value or 24.0),
                "cholesterol": float(chol_input.value or 180),
                "hba1c": float(hba1c_input.value or 5.5)
            }
            
            res = state.predict_sanjeevani_risk(data)
            
            risk_label = res["predicted_risk"]
            confidence = res["confidence"]
            color = res["risk_color"]
            advice = res["clinical_advice"]
            probs = res.get("probabilities", {})

            # Update result container
            result_container.controls = [
                ft.Card(
                    elevation=2,
                    content=ft.Container(
                        content=ft.Column([
                            ft.Row([
                                ft.Icon(ft.Icons.HEALTH_AND_SAFETY_ROUNDED, size=28, color=color),
                                ft.Text(f"Predicted Risk: {risk_label}", size=16, weight=ft.FontWeight.BOLD, color=color),
                            ], spacing=8),
                            ft.Text(f"Model Confidence: {confidence}% (Random Forest Classifier)", size=12, color=ft.Colors.GREY_700),
                            ft.ProgressBar(
                                value=confidence / 100.0 if risk_label != "Low Risk" else 0.25,
                                color=color,
                                bgcolor=ft.Colors.GREY_200,
                                height=8
                            ),
                            ft.Row([
                                ft.Text(f"Low: {probs.get('Low Risk', 0)}%", size=11, color=ft.Colors.GREEN_700),
                                ft.Text(f"Moderate: {probs.get('Moderate Risk', 0)}%", size=11, color=ft.Colors.AMBER_700),
                                ft.Text(f"High: {probs.get('High Risk', 0)}%", size=11, color=ft.Colors.RED_700),
                            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                            ft.Divider(height=10),
                            ft.Text(f"💡 Clinical Recommendation: {advice}", size=12, color=ft.Colors.GREY_900)
                        ], spacing=6),
                        padding=16,
                        border_radius=12
                    )
                )
            ]
            result_container.visible = True
            loading_ring.visible = False
            predict_btn.disabled = False
            page.update()

        except Exception as ex:
            loading_ring.visible = False
            predict_btn.disabled = False
            show_snackbar(page, f"Error predicting risk: {str(ex)}", bgcolor="#DC2626")
            page.update()

    predict_btn = ft.FilledButton(
        content=ft.Row([
            ft.Icon(ft.Icons.ANALYTICS_ROUNDED),
            ft.Text("Calculate Disease Risk", weight=ft.FontWeight.BOLD),
            loading_ring
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
        style=ft.ButtonStyle(
            bgcolor=ft.Colors.INDIGO_700,
            color=ft.Colors.WHITE,
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=48,
        on_click=run_prediction
    )

    return ft.ListView(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.MONITOR_HEART_ROUNDED, color=ft.Colors.INDIGO_700),
                ft.Text("Sanjeevani Risk Diagnostic ML", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=8),
            ft.Text(
                "Supervised Machine Learning pipeline (StandardScaler + RandomForest) predicting patient clinical risk severity.",
                size=12, color=ft.Colors.GREY_600
            ),
            ft.Container(height=6),
            ft.Row([age_input, bmi_input]),
            ft.Row([sugar_input, hba1c_input]),
            ft.Row([bp_sys_input, bp_dia_input]),
            ft.Row([chol_input]),
            ft.Container(height=8),
            predict_btn,
            ft.Container(height=8),
            result_container,
            ft.Container(height=20)
        ],
        spacing=8,
        padding=16
    )
