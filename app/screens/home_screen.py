import flet as ft
from app.state import state

def build_home_screen(page: ft.Page, navigate_to) -> ft.Control:
    backend_ok = state.check_backend_connection()
    status_color = ft.Colors.GREEN_500 if backend_ok else ft.Colors.RED_500
    status_text = "AI Server Online" if backend_ok else "Server Offline (Run run_backend.py)"

    header_card = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Row([
                    ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED, color=ft.Colors.WHITE, size=28),
                    ft.Text("MedScan AI", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ]),
                ft.Container(
                    content=ft.Row([
                        ft.Container(width=8, height=8, border_radius=4, bgcolor=status_color),
                        ft.Text(status_text, size=11, color=ft.Colors.WHITE70, weight=ft.FontWeight.W_500),
                    ], spacing=4),
                    padding=ft.padding.symmetric(horizontal=8, vertical=4),
                    border_radius=12,
                    bgcolor=ft.Colors.WHITE12,
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("Sanjeevani Pocket Health Diagnostic & OCR Assistant", size=13, color=ft.Colors.WHITE70),
            ft.Divider(color=ft.Colors.WHITE24, height=15),
            ft.Row([
                ft.CircleAvatar(
                    content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.TEAL_900),
                    bgcolor=ft.Colors.WHITE,
                    radius=18
                ),
                ft.Column([
                    ft.Text("Welcome, Vikash Kumawat", size=15, weight=ft.FontWeight.W_600, color=ft.Colors.WHITE),
                    ft.Text("BCA Data Science & AI Engineer", size=11, color=ft.Colors.WHITE70),
                ], spacing=1)
            ], spacing=10)
        ], spacing=8),
        padding=18,
        border_radius=16,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=[ft.Colors.TEAL_800, ft.Colors.CYAN_900]
        ),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK12)
    )

    action_scan = ft.Card(
        elevation=2,
        content=ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.DOCUMENT_SCANNER_ROUNDED, size=36, color=ft.Colors.TEAL_700),
                ft.Text("Scan Medical Report", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("Prescriptions, CBC, Blood Sugar, Lipid Profiles OCR & AI", size=11, color=ft.Colors.GREY_600),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=16,
            border_radius=12,
            ink=True,
            on_click=lambda _: navigate_to(1),
            width=170,
            height=140
        )
    )

    action_risk = ft.Card(
        elevation=2,
        content=ft.Container(
            content=ft.Column([
                ft.Icon(ft.Icons.HEALTH_AND_SAFETY_ROUNDED, size=36, color=ft.Colors.INDIGO_600),
                ft.Text("Sanjeevani Risk ML", size=14, weight=ft.FontWeight.BOLD),
                ft.Text("Predict Disease Risk via Trained ML Classifier", size=11, color=ft.Colors.GREY_600),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=16,
            border_radius=12,
            ink=True,
            on_click=lambda _: navigate_to(3),
            width=170,
            height=140
        )
    )

    tip_card = ft.Card(
        elevation=1,
        content=ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Icon(ft.Icons.LIGHTBULB_OUTLINE_ROUNDED, color=ft.Colors.AMBER_700, size=20),
                    ft.Text("Daily Clinical Tip", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.AMBER_900),
                ], spacing=6),
                ft.Text(
                    "Fasting Blood Sugar 70-100 mg/dL aur BP 120/80 mmHg ideal hota hai. Agar values borderline hain toh daily 30 min walk aur sodium control se naturally stabilize ho sakti hain.",
                    size=12,
                    color=ft.Colors.GREY_800
                )
            ], spacing=6),
            padding=14,
            border_radius=12,
            bgcolor=ft.Colors.AMBER_50
        )
    )

    history_preview = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Text("Recent Diagnostic Scans", size=15, weight=ft.FontWeight.BOLD),
                ft.TextButton("View All", on_click=lambda _: navigate_to(4))
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Text("Open Scanner to process your first medical report.", size=12, color=ft.Colors.GREY_600)
        ]),
        padding=ft.padding.only(top=10)
    )

    return ft.ListView(
        controls=[
            header_card,
            ft.Container(height=12),
            ft.Text("Quick Actions", size=16, weight=ft.FontWeight.BOLD),
            ft.Row([action_scan, action_risk], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Container(height=12),
            tip_card,
            history_preview
        ],
        spacing=8,
        padding=16
    )
