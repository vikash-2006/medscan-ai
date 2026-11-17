import os
import flet as ft
from app.state import state

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

ROBOT_IMG = _get_asset("robot_avatar.jpg")

def build_sanjeevani_user_profile_screen(page: ft.Page, navigate_to) -> ft.Control:
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("9:41", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color="#0F172A"),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color="#0F172A"),
                ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=16, color="#0F172A"),
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    header = ft.Container(
        content=ft.Row([
            ft.Text("Patient Profile", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(
                content=ft.Icon(ft.Icons.EDIT_OUTLINED, color="#2563EB", size=18),
                width=38,
                height=38,
                border_radius=19,
                bgcolor="#EAF4FF",
                alignment=ft.Alignment.CENTER,
                ink=True
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=8)
    )

    # Profile Avatar & Bio Card
    bio_card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Image(src=ROBOT_IMG, width=80, height=80, fit=ft.BoxFit.COVER, border_radius=40),
                width=80,
                height=80,
                border_radius=40,
                border=ft.Border.all(3, "#2563EB")
            ),
            ft.Container(height=4),
            ft.Text(state.patient_name, size=18, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Text("BCA Data Science & AI Engineer", size=12, color="#64748B"),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.VERIFIED_ROUNDED, size=14, color="#2563EB"),
                    ft.Text("ABHA ID: 91-4421-8890-2134", size=11, weight=ft.FontWeight.BOLD, color="#2563EB")
                ], spacing=4),
                padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                border_radius=10,
                bgcolor="#EAF4FF"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=ft.Padding.symmetric(vertical=10),
        alignment=ft.Alignment.CENTER
    )

    # Emergency SOS One-Tap Button
    sos_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.EMERGENCY_ROUNDED, color=ft.Colors.WHITE, size=24),
                width=42,
                height=42,
                border_radius=21,
                bgcolor="#DC2626",
                alignment=ft.Alignment.CENTER
            ),
            ft.Column([
                ft.Text("Emergency SOS Dispatcher", size=13, weight=ft.FontWeight.BOLD, color="#991B1B"),
                ft.Text("1-Tap 108 Ambulance & GPS Sharing", size=11, color="#DC2626"),
            ], expand=True, spacing=1),
            ft.Icon(ft.Icons.CALL_ROUNDED, color="#DC2626", size=20)
        ], spacing=10),
        padding=14,
        border_radius=18,
        bgcolor="#FEF2F2",
        border=ft.Border.all(1, "#FECACA"),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        ink=True,
        on_click=lambda _: page.open(ft.SnackBar(ft.Text("Emergency 108 Alert Triggered with live GPS!"), bgcolor="#DC2626"))
    )

    # Health Vitals Summary Row
    def create_vital_pill(label: str, val: str):
        return ft.Container(
            content=ft.Column([
                ft.Text(label, size=10, color="#64748B"),
                ft.Text(val, size=13, weight=ft.FontWeight.BOLD, color="#0F172A")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
            width=100,
            padding=ft.Padding.symmetric(vertical=10),
            bgcolor=ft.Colors.WHITE,
            border_radius=14,
            border=ft.Border.all(1, "#E2E8F0")
        )

    vitals_row = ft.Container(
        content=ft.Row([
            create_vital_pill("Blood Group", "O+ Positive"),
            create_vital_pill("Avg Fasting", "120 mg/dL"),
            create_vital_pill("BMI Index", "25.5 kg/m²"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # Settings Menu Items
    def create_menu_tile(icon_data, title: str, subtitle: str, on_click=None):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(icon_data, color="#2563EB", size=20),
                    width=38,
                    height=38,
                    border_radius=12,
                    bgcolor="#EAF4FF",
                    alignment=ft.Alignment.CENTER
                ),
                ft.Column([
                    ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text(subtitle, size=11, color="#64748B"),
                ], expand=True, spacing=1),
                ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=14, color="#94A3B8")
            ], spacing=10),
            padding=12,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            margin=ft.Padding.symmetric(horizontal=18, vertical=4),
            ink=True,
            on_click=on_click
        )

    return ft.ListView(
        controls=[
            status_bar,
            header,
            bio_card,
            sos_card,
            vitals_row,
            ft.Container(height=6),
            create_menu_tile(ft.Icons.SHIELD_OUTLINED, "Health Insurance", "Star Health Comprehensive (Active)"),
            create_menu_tile(ft.Icons.DOCUMENT_SCANNER_ROUNDED, "My Scanned Reports", "View OCR Biomarkers & History", on_click=lambda _: navigate_to("reports")),
            create_menu_tile(ft.Icons.PSYCHOLOGY_ROUNDED, "Sanjeevani Risk ML", "Trained Random Forest Classifier", on_click=lambda _: navigate_to("risk_ml")),
            create_menu_tile(ft.Icons.TRANSLATE_ROUNDED, "Language & Region", "English / Hinglish (Active)"),
            create_menu_tile(ft.Icons.HELP_OUTLINE_ROUNDED, "Sanjeevani 24/7 Helpline", "Call +91 141-SANJEEVANI"),
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
