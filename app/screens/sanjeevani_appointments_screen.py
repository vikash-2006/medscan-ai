import os
import flet as ft
from app.state import state
from app.utils import show_snackbar, show_dialog_modal, trigger_haptic

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

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
                content=ft.Icon(ft.Icons.ADD_ROUNDED, color="#2563EB", size=22),
                width=38,
                height=38,
                border_radius=19,
                bgcolor="#EAF4FF",
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: navigate_to("doctors")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=8)
    )

    # Get active appointment from state
    active_appt = state.booked_appointments[0] if state.booked_appointments else {
        "doctor_name": "Dr. Rohan Mehta",
        "specialty": "General Physician • Consultation",
        "date_str": "Tue, 17 Nov 2026",
        "time_str": "11:00 AM",
        "status": "Confirmed",
        "avatar": "doctor_portrait.jpg",
        "fee": "₹500"
    }

    doc_avatar = _get_asset(active_appt.get("avatar", "doctor_portrait.jpg"))

    def cancel_active_appointment(e):
        state.cancel_active_appointment(0)
        show_snackbar(page, "Appointment successfully cancelled in database.", bgcolor="#DC2626")
        page.update()
        navigate_to("appointments")

    # 3. Upcoming Appointment Pass Card
    active_pass = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Row([
                    ft.Image(src=doc_avatar, width=48, height=48, fit=ft.BoxFit.COVER, border_radius=14),
                    ft.Column([
                        ft.Text(active_appt.get("doctor_name", "Doctor"), size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text(active_appt.get("specialty", "Specialist"), size=11, color=ft.Colors.with_opacity(0.85, ft.Colors.WHITE)),
                    ], spacing=1)
                ], spacing=10),
                ft.Container(
                    content=ft.Text(active_appt.get("status", "Confirmed"), size=10, weight=ft.FontWeight.BOLD, color="#16A34A"),
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
                        ft.Text(active_appt.get("date_str", "Today"), size=11, weight=ft.FontWeight.BOLD, color="#1D4ED8")
                    ], spacing=4),
                    ft.Container(width=1, height=14, bgcolor="#CBD5E1"),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color="#1D4ED8"),
                        ft.Text(active_appt.get("time_str", "10:00 AM"), size=11, weight=ft.FontWeight.BOLD, color="#1D4ED8")
                    ], spacing=4)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                border_radius=12,
                bgcolor=ft.Colors.WHITE
            ),

            ft.Container(height=10),
            # Actions Row: Join Video Call, Reschedule & Cancel
            ft.Row([
                ft.FilledButton(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, size=16),
                        ft.Text("Join Video", size=11, weight=ft.FontWeight.BOLD)
                    ], spacing=4),
                    style=ft.ButtonStyle(
                        bgcolor="#16A34A",
                        color=ft.Colors.WHITE,
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    expand=True,
                    height=42,
                    on_click=lambda e: (navigate_to("video_call"), trigger_haptic(page))
                ),
                ft.OutlinedButton(
                    content=ft.Text("Reschedule", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ft.Colors.WHITE_70),
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    height=42,
                    on_click=lambda e: (navigate_to("doctors"), trigger_haptic(page))
                ),
                ft.OutlinedButton(
                    content=ft.Icon(ft.Icons.CANCEL_OUTLINED, size=16, color=ft.Colors.WHITE),
                    style=ft.ButtonStyle(
                        side=ft.BorderSide(1, ft.Colors.WHITE_70),
                        shape=ft.RoundedRectangleBorder(radius=12)
                    ),
                    height=42,
                    tooltip="Cancel Appointment",
                    on_click=cancel_active_appointment
                )
            ], spacing=6)
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
    def show_qr_modal(e):
        doc_name = active_appt.get("doctor_name", "Doctor")
        d_str = active_appt.get("date_str", "Today")
        t_str = active_appt.get("time_str", "10:00 AM")
        qr_content = ft.Column([
            ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, size=120, color="#2563EB"),
            ft.Text(f"Token #SJH-4409\n{doc_name}", size=13, weight=ft.FontWeight.BOLD,
                    text_align=ft.TextAlign.CENTER, color="#0F172A"),
            ft.Text(f"{d_str} • {t_str}\nPresent at Sanjeevani Kiosk reception counter.",
                    size=11, color="#64748B", text_align=ft.TextAlign.CENTER)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6)
        show_dialog_modal(page, "Digital Check-In Pass", qr_content)

    qr_card = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.QR_CODE_2_ROUNDED, size=46, color="#2563EB"),
            ft.Column([
                ft.Text("Digital Clinic Check-in Pass", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("Tap to view QR barcode pass for fast-track entry.", size=11, color="#64748B"),
            ], expand=True, spacing=2),
            ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=14, color="#94A3B8")
        ], spacing=10),
        padding=14,
        border_radius=18,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#E2E8F0"),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000")),
        ink=True,
        on_click=show_qr_modal
    )

    # 5. Past Visits History
    def create_history_card(doc_name: str, spec: str, date_str: str, status: str):
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color="#16A34A", size=22),
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor="#DCFCE7",
                    alignment=ft.Alignment.CENTER
                ),
                ft.Column([
                    ft.Text(doc_name, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text(f"{spec} • {date_str}", size=11, color="#64748B"),
                ], expand=True, spacing=1),
                ft.Container(
                    content=ft.Text("Report", size=11, weight=ft.FontWeight.BOLD, color="#2563EB"),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                    border_radius=8,
                    bgcolor="#EAF4FF",
                    ink=True,
                    on_click=lambda _: navigate_to("reports")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=12,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            margin=ft.Padding.symmetric(horizontal=18, vertical=4)
        )

    history_section = ft.Column([
        ft.Container(
            content=ft.Text("Past Consultations", size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
            padding=ft.Padding.symmetric(horizontal=18, vertical=6)
        ),
        create_history_card("Dr. Ananya Sharma", "Cardiologist", "12 Oct 2026", "Completed"),
        create_history_card("Dr. Vivek Singh", "Gastroenterologist", "24 Aug 2026", "Completed"),
    ], spacing=4)

    return ft.ListView(
        controls=[
            status_bar,
            header,
            active_pass,
            qr_card,
            history_section,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
