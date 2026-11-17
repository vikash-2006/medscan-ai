import os
import flet as ft
from app.state import state

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_ROHAN = _get_asset("doctor_portrait.jpg")

def build_sanjeevani_appointments_screen(page: ft.Page, navigate_to) -> ft.Control:
    # 1. Top Status Bar
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

    # 2. Header
    header = ft.Container(
        content=ft.Row([
            ft.Text("My Appointments", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(
                content=ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color="#2563EB", size=20),
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

    # 3. Upcoming Appointment Pass Card
    active_pass = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Row([
                    ft.Image(src=DOCTOR_ROHAN, width=48, height=48, fit=ft.BoxFit.COVER, border_radius=14),
                    ft.Column([
                        ft.Text("Dr. Rohan Mehta", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("General Physician • Consultation", size=11, color=ft.Colors.with_opacity(0.85, ft.Colors.WHITE)),
                    ], spacing=1)
                ], spacing=10),
                ft.Container(
                    content=ft.Text("Confirmed", size=10, weight=ft.FontWeight.BOLD, color="#16A34A"),
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=8,
                    bgcolor=ft.Colors.WHITE
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(height=8),
            # Date & Time Pill
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, size=14, color="#1D4ED8"),
                        ft.Text("Tue, 17 Nov 2026", size=11, weight=ft.FontWeight.BOLD, color="#1D4ED8")
                    ], spacing=4),
                    ft.Container(width=1, height=14, bgcolor="#CBD5E1"),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color="#1D4ED8"),
                        ft.Text("11:00 AM", size=11, weight=ft.FontWeight.BOLD, color="#1D4ED8")
                    ], spacing=4)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=12,
                bgcolor=ft.Colors.WHITE
            ),

            ft.Container(height=10),
            # Actions Row
            ft.Row([
                ft.FilledButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, size=16),
                        ft.Text("Join Video Call", size=12, weight=ft.FontWeight.BOLD)
                    ], spacing=6),
                    style=ft.ButtonStyle(
                        bgcolor="#16A34A",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    expand=True,
                    height=40,
                    on_click=lambda _: navigate_to("video_call")
                ),
                ft.OutlinedButton(
                    content=ft.Text("Reschedule", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ft.Colors.WHITE70),
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    height=40,
                    on_click=lambda _: navigate_to("doctors")
                )
            ], spacing=8)
        ], spacing=4),
        padding=16,
        border_radius=22,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#2563EB", "#1D4ED8"]
        ),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=16, color=ft.Colors.with_opacity(0.25, "#2563EB"))
    )

    # 4. QR Code Digital Check-in
    qr_card = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, size=48, color="#2563EB"),
            ft.Column([
                ft.Text("Digital Clinic Check-in Pass", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("Scan this QR code upon arrival at Sanjeevani Clinic.", size=11, color="#64748B"),
            ], expand=True, spacing=2),
            ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=14, color="#94A3B8")
        ], spacing=10),
        padding=14,
        border_radius=18,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#E2E8F0"),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000"))
    )

    # 5. Past Visits History
    past_header = ft.Container(
        content=ft.Text("Past Consultations", size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    def create_past_visit(name: str, date: str, diagnosis: str):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#16A34A", size=24),
                    width=42,
                    height=42,
                    border_radius=12,
                    bgcolor="#DCFCE7",
                    alignment=ft.Alignment.CENTER
                ),
                ft.Column([
                    ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text(f"{diagnosis} • {date}", size=11, color="#64748B"),
                ], expand=True, spacing=1),
                ft.TextButton("Rx Slip", on_click=lambda _: navigate_to("reports"))
            ], spacing=10),
            padding=12,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            margin=ft.Padding.symmetric(horizontal=18, vertical=4)
        )

    return ft.ListView(
        controls=[
            status_bar,
            header,
            active_pass,
            qr_card,
            past_header,
            create_past_visit("Dr. Ananya Sharma", "12 Oct 2026", "Lipid & BP Consultation"),
            create_past_visit("Dr. Vivek Singh", "28 Aug 2026", "Digestive Health Checkup"),
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
