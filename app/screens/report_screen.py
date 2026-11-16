import flet as ft
from app.state import state

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
                ft.ElevatedButton("Go to Scanner", icon=ft.Icons.DOCUMENT_SCANNER_ROUNDED, on_click=lambda _: navigate_to(1))
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.alignment.center,
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
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=20,
        bgcolor=urgency_bg,
        border=ft.border.all(1, urgency_color)
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
                        padding=ft.padding.symmetric(horizontal=8, vertical=4),
                        border_radius=8,
                        bgcolor=badge_bg
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=ft.padding.symmetric(vertical=6, horizontal=8),
                border=ft.border.only(bottom=ft.BorderSide(0.5, ft.Colors.GREY_300))
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
        on_click=lambda _: navigate_to(3)
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
            ft.Container(height=20)
        ],
        spacing=8,
        padding=16
    )
