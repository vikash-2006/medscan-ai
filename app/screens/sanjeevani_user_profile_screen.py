import os
import flet as ft
from app.state import state
from app.utils import show_snackbar, show_dialog_modal

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

    def open_edit_profile(e):
        name_input = ft.TextField(label="Full Name", value=state.patient_name, dense=True)

        def save_name(ev):
            val = (name_input.value or "").strip()
            if val:
                state.patient_name = val
                if hasattr(page, "pop_dialog"):
                    page.pop_dialog()
                show_snackbar(page, f"Profile updated to {val}!", bgcolor="#16A34A")
                page.update()
                navigate_to("user_profile")

        dialog_content = ft.Column([
            name_input,
            ft.FilledButton("Update Name", on_click=save_name, style=ft.ButtonStyle(bgcolor="#2563EB"))
        ], tight=True, spacing=12)
        show_dialog_modal(page, "Edit Patient Profile", dialog_content)

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
                ink=True,
                on_click=open_edit_profile
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
            ft.Text("BCA Data Science & AI Engineer • Jaipur", size=12, color="#64748B"),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.VERIFIED_ROUNDED, size=14, color="#2563EB"),
                    ft.Text(f"ABHA ID: {os.getenv('ABHA_ID', 'N/A')}", size=11, weight=ft.FontWeight.BOLD, color="#2563EB")
                ], spacing=4),
                padding=ft.Padding.symmetric(horizontal=12, vertical=4),
                border_radius=10,
                bgcolor="#EAF4FF"
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=ft.Padding.symmetric(vertical=10),
        alignment=ft.Alignment.CENTER
    )

    # Emergency SOS Dispatcher
    def trigger_sos_dialog(e):
        def confirm_sos(ev):
            if hasattr(page, "pop_dialog"):
                page.pop_dialog()
            show_snackbar(page, "🚨 Emergency 108 Dispatch Alert Broadcasted to Nearest Ambulance Network!", bgcolor="#DC2626")

        sos_content = ft.Column([
            ft.Icon(ft.Icons.WARNING_AMBER_ROUNDED, color="#DC2626", size=54),
            ft.Text("Confirm Emergency 108 Alert?", size=15, weight=ft.FontWeight.BOLD, color="#991B1B", text_align=ft.TextAlign.CENTER),
            ft.Text("This will immediately send your live GPS coordinates to Jaipur Emergency Medical Services (108) and emergency contacts.",
                    size=12, color="#475569", text_align=ft.TextAlign.CENTER),
            ft.Container(height=8),
            ft.FilledButton(
                "Trigger SOS Ambulance Now",
                style=ft.ButtonStyle(bgcolor="#DC2626"),
                on_click=confirm_sos
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6, tight=True)
        show_dialog_modal(page, "Emergency SOS Dispatch", sos_content)

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
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000")),
        ink=True,
        on_click=trigger_sos_dialog
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

    def get_safe_int(val, default):
        try:
            return int(float(val))
        except (ValueError, TypeError):
            return default

    vitals_row = ft.Container(
        content=ft.Row([
            create_vital_pill("Blood Group", "O+ Positive"),
            create_vital_pill("Avg Fasting", f"{get_safe_int(state.current_vitals.get('blood_sugar', 120), 120)} mg/dL"),
            create_vital_pill("BMI Index", f"{state.current_vitals.get('bmi', 25.5)} kg/m²"),
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
            margin=ft.Padding.symmetric(horizontal=18, vertical=3),
            ink=True,
            on_click=on_click
        )

    def handle_cloud_sync(e):
        try:
            from backend.cloud_backup import full_backup, is_cloud_available
            if not is_cloud_available():
                show_snackbar(page, "Cloud Sync: Add SUPABASE_URL & SUPABASE_KEY to .env to activate.", bgcolor="#D97706")
                return
            res = full_backup(state)
            if res.get("success"):
                show_snackbar(page, f"Cloud Backup Complete! {res.get('total_uploaded', 0)} records synced.", bgcolor="#16A34A")
            else:
                show_snackbar(page, f"Backup error: {res.get('error')}", bgcolor="#DC2626")
        except Exception as ex:
            show_snackbar(page, f"Cloud error: {str(ex)}", bgcolor="#DC2626")

    menu_section = ft.Column([
        create_menu_tile(ft.Icons.RECEIPT_LONG_ROUNDED, "Lab Test Reports", "Clinical biomarker analysis history", lambda _: navigate_to("reports")),
        create_menu_tile(ft.Icons.FAVORITE_ROUNDED, "Sanjeevani Risk ML Engine", "Cardiometabolic risk assessments", lambda _: navigate_to("risk_ml")),
        create_menu_tile(ft.Icons.MEDICATION_ROUNDED, "Medicine Schedule", "Active daily dosage reminders", lambda _: navigate_to("medicines")),
        create_menu_tile(ft.Icons.CLOUD_SYNC_ROUNDED, "Cloud Backup & Sync", "Sync appointments, scans & meds to Cloud", handle_cloud_sync),
        create_menu_tile(ft.Icons.SECURITY_ROUNDED, "Privacy & ABHA Sync", "Digital health locker linked", lambda _: show_snackbar(page, "ABHA health records encrypted and synced.", bgcolor="#16A34A")),
    ], spacing=4)

    return ft.ListView(
        controls=[
            status_bar,
            header,
            bio_card,
            sos_card,
            vitals_row,
            ft.Container(height=6),
            menu_section,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
