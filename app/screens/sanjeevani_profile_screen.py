import os
import flet as ft
from app.state import state

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_ROHAN = _get_asset("doctor_portrait.jpg")

def build_sanjeevani_profile_screen(page: ft.Page, navigate_to) -> ft.Control:
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

    # 2. Top Header with Back, Heart Favorite, and Share Icons
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color="#0F172A", size=18),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: navigate_to("doctors")
            ),
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, color="#0F172A", size=18),
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, "#E2E8F0"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    on_click=lambda _: page.open(ft.SnackBar(ft.Text("Added Dr. Rohan Mehta to favorites!")))
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.SHARE_OUTLINED, color="#0F172A", size=18),
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, "#E2E8F0"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    on_click=lambda _: page.open(ft.SnackBar(ft.Text("Doctor profile link copied!")))
                ),
            ], spacing=8)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 3. Doctor Portrait & Identity Info
    doctor_info_card = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Image(
                    src=DOCTOR_ROHAN,
                    width=90,
                    height=90,
                    fit=ft.BoxFit.COVER,
                    border_radius=24
                ),
                width=90,
                height=90,
                border_radius=24,
                border=ft.Border.all(3, "#EAF4FF"),
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color=ft.Colors.with_opacity(0.1, "#000000"))
            ),
            ft.Container(height=4),
            ft.Row([
                ft.Text("Dr. Rohan Mehta", size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Icon(ft.Icons.VERIFIED_ROUNDED, size=18, color="#2563EB")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
            ft.Text("General Physician", size=13, color="#64748B"),
            ft.Row([
                ft.Icon(ft.Icons.STAR_ROUNDED, size=16, color="#F59E0B"),
                ft.Text("4.8", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("(1,240 Reviews)", size=12, color="#94A3B8"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=3)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=ft.Padding.symmetric(vertical=8),
        alignment=ft.Alignment.CENTER
    )

    # 4. Three Stat Badges (Years, Patients, Rating)
    def create_stat_card(icon_data, value: str, label: str):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon_data, color="#2563EB", size=22),
                ft.Text(value, size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text(label, size=11, color="#64748B")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            width=100,
            padding=ft.Padding.symmetric(vertical=12, horizontal=8),
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000"))
        )

    stats_row = ft.Container(
        content=ft.Row([
            create_stat_card(ft.Icons.HISTORY_TOGGLE_OFF_ROUNDED, "7+", "Years"),
            create_stat_card(ft.Icons.PEOPLE_ALT_ROUNDED, "2.5K+", "Patients"),
            create_stat_card(ft.Icons.STAR_ROUNDED, "98%", "Rating"),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 5. Segmented Tab Pills [Book | About | Reviews]
    active_tab = "Book"
    segmented_tabs = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Text("Book", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.Padding.symmetric(horizontal=24, vertical=8),
                border_radius=14,
                bgcolor="#2563EB",
                expand=True,
                alignment=ft.Alignment.CENTER
            ),
            ft.Container(
                content=ft.Text("About", size=13, weight=ft.FontWeight.W_500, color="#64748B"),
                padding=ft.Padding.symmetric(horizontal=24, vertical=8),
                border_radius=14,
                expand=True,
                alignment=ft.Alignment.CENTER
            ),
            ft.Container(
                content=ft.Text("Reviews", size=13, weight=ft.FontWeight.W_500, color="#64748B"),
                padding=ft.Padding.symmetric(horizontal=24, vertical=8),
                border_radius=14,
                expand=True,
                alignment=ft.Alignment.CENTER
            )
        ]),
        padding=4,
        border_radius=18,
        bgcolor="#F1F5F9",
        margin=ft.Padding.symmetric(horizontal=18, vertical=8)
    )

    # 6. "Select Date" Section (Calendar Selector Pills)
    selected_date = "Tue 17 Nov"

    def create_date_pill(day: str, date: str, is_active: bool = False):
        if is_active:
            return ft.Container(
                content=ft.Column([
                    ft.Text(day, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text(date, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                border_radius=16,
                bgcolor="#2563EB",
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.3, "#2563EB")),
                ink=True
            )
        else:
            return ft.Container(
                content=ft.Column([
                    ft.Text(day, size=11, color="#64748B"),
                    ft.Text(date, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                border_radius=16,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                ink=True
            )

    date_section = ft.Container(
        content=ft.Column([
            ft.Text("Select Date", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Row([
                create_date_pill("Tue", "17 Nov", True),
                create_date_pill("Wed", "18 Nov", False),
                create_date_pill("Thu", "19 Nov", False),
                create_date_pill("Fri", "20 Nov", False),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=8),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 7. "Select Time" Section (Time Slot Selector Pills)
    selected_time = "11:00 AM"

    def create_time_pill(time_str: str, is_active: bool = False):
        if is_active:
            return ft.Container(
                content=ft.Text(time_str, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                border_radius=14,
                bgcolor="#2563EB",
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.3, "#2563EB")),
                ink=True
            )
        else:
            return ft.Container(
                content=ft.Text(time_str, size=12, weight=ft.FontWeight.W_500, color="#0F172A"),
                padding=ft.Padding.symmetric(horizontal=16, vertical=10),
                border_radius=14,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                ink=True
            )

    time_section = ft.Container(
        content=ft.Column([
            ft.Text("Select Time", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Row([
                create_time_pill("10:00 AM", False),
                create_time_pill("11:00 AM", True),
                create_time_pill("12:00 PM", False),
            ], spacing=10)
        ], spacing=8),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 8. Bottom CTA Button: "Confirm Booking"
    def handle_confirm_booking(e):
        page.open(
            ft.SnackBar(
                ft.Text("Appointment Confirmed with Dr. Rohan Mehta on Tue 17 Nov at 11:00 AM!"),
                bgcolor="#16A34A"
            )
        )
        navigate_to("appointments")

    confirm_btn = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color=ft.Colors.WHITE, size=18),
            ft.Text("Confirm Booking", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        height=52,
        border_radius=26,
        bgcolor="#2563EB",
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=16, color=ft.Colors.with_opacity(0.35, "#2563EB")),
        ink=True,
        on_click=handle_confirm_booking
    )

    bottom_action_bar = ft.Container(
        content=confirm_btn,
        padding=ft.Padding.symmetric(horizontal=18, vertical=10),
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.only(top=ft.BorderSide(1, "#E2E8F0"))
    )

    # Scrollable Assembly
    return ft.Column([
        ft.Container(
            content=ft.ListView(
                controls=[
                    status_bar,
                    header,
                    doctor_info_card,
                    stats_row,
                    segmented_tabs,
                    date_section,
                    time_section,
                    ft.Container(height=20)
                ],
                spacing=4,
                padding=0
            ),
            expand=True
        ),
        bottom_action_bar
    ], expand=True, spacing=0)
