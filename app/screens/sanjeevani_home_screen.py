import os
import flet as ft
from app.state import state

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_MALE_1 = _get_asset("doctor_portrait.jpg")
DOCTOR_FEMALE = _get_asset("doctor_female.jpg")
ROBOT_IMG = _get_asset("robot_avatar.jpg")

def build_sanjeevani_home_screen(page: ft.Page, navigate_to) -> ft.Control:
    # 1. Status Bar (9:41, wifi, battery)
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

    # 2. Header: Avatar + "Hi, Vikash 👋" + Notification Bell
    header_section = ft.Container(
        content=ft.Row([
            ft.Row([
                # Avatar Circle with subtle blue ring
                ft.Container(
                    content=ft.Image(
                        src=ROBOT_IMG,
                        width=42,
                        height=42,
                        fit=ft.BoxFit.COVER,
                        border_radius=21
                    ),
                    width=42,
                    height=42,
                    border_radius=21,
                    border=ft.Border.all(2, "#2563EB")
                ),
                ft.Column([
                    ft.Text(f"Hi, {state.patient_name.split()[0]} 👋", size=17, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("How are you feeling today?", size=11, color="#64748B"),
                ], spacing=1)
            ], spacing=10),

            # Notification Bell Icon with Red Alert Badge
            ft.Stack([
                ft.Container(
                    content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color="#0F172A", size=22),
                    width=40,
                    height=40,
                    border_radius=20,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, "#E2E8F0"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    on_click=lambda _: page.open(ft.SnackBar(ft.Text("Your Sanjeevani health sync is active!")))
                ),
                ft.Container(
                    width=9,
                    height=9,
                    border_radius=4.5,
                    bgcolor="#EF4444",
                    right=2,
                    top=2
                )
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=8)
    )

    # 3. Modern Rounded Search Bar with Filter Sliders Icon
    search_bar = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.SEARCH_ROUNDED, color="#94A3B8", size=20),
            ft.TextField(
                hint_text="Search doctors, specialties...",
                dense=True,
                border=ft.InputBorder.NONE,
                text_size=13,
                expand=True,
                hint_style=ft.TextStyle(color="#94A3B8", size=13),
                on_submit=lambda _: navigate_to("doctors")
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.TUNE_ROUNDED, color="#2563EB", size=18),
                width=32,
                height=32,
                border_radius=10,
                bgcolor="#EAF4FF",
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: navigate_to("doctors")
            )
        ], spacing=8),
        bgcolor=ft.Colors.WHITE,
        border_radius=18,
        border=ft.Border.all(1, "#E2E8F0"),
        padding=ft.Padding.symmetric(horizontal=14, vertical=4),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.04, "#000000"))
    )

    # 4. Hero Banner Card: "Consult a Doctor" (Royal Blue Gradient + Doctor Portrait)
    consult_banner = ft.Container(
        content=ft.Row([
            # Left Text & CTA
            ft.Column([
                ft.Text("Consult a Doctor", size=18, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Text("Online or In-Clinic", size=12, color=ft.Colors.with_opacity(0.85, ft.Colors.WHITE)),
                ft.Container(height=6),
                ft.Container(
                    content=ft.Row([
                        ft.Text("Book Now", size=12, weight=ft.FontWeight.BOLD, color="#2563EB"),
                        ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=14, color="#2563EB")
                    ], spacing=4),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    border_radius=16,
                    bgcolor=ft.Colors.WHITE,
                    ink=True,
                    on_click=lambda _: navigate_to("doctors")
                )
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2, expand=True),

            # Right Doctor Portrait
            ft.Container(
                content=ft.Image(
                    src=DOCTOR_MALE_1,
                    width=96,
                    height=100,
                    fit=ft.BoxFit.COVER,
                    border_radius=16
                ),
                width=96,
                height=100,
                border_radius=16,
                alignment=ft.Alignment.CENTER
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.all(18),
        border_radius=22,
        gradient=ft.LinearGradient(
            begin=ft.Alignment.TOP_LEFT,
            end=ft.Alignment.BOTTOM_RIGHT,
            colors=["#2563EB", "#1D4ED8"]
        ),
        margin=ft.Padding.symmetric(horizontal=18, vertical=8),
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=16,
            color=ft.Colors.with_opacity(0.25, "#2563EB")
        )
    )

    # 5. Quick 6-Category Grid (Doctors, Appointments, Medicines, Lab Tests, Reports, More)
    def create_category_card(title: str, icon_data, target_screen):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon_data, color="#2563EB", size=24),
                    width=48,
                    height=48,
                    border_radius=16,
                    bgcolor="#EAF4FF",
                    alignment=ft.Alignment.CENTER
                ),
                ft.Text(title, size=11, weight=ft.FontWeight.W_600, color="#0F172A")
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            width=100,
            padding=ft.Padding.symmetric(horizontal=8, vertical=12),
            bgcolor=ft.Colors.WHITE,
            border_radius=18,
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000")),
            ink=True,
            on_click=lambda _: navigate_to(target_screen)
        )

    categories_grid = ft.Container(
        content=ft.Column([
            ft.Row([
                create_category_card("Doctors", ft.Icons.LOCAL_HOSPITAL_ROUNDED, "doctors"),
                create_category_card("Appointments", ft.Icons.CALENDAR_MONTH_ROUNDED, "appointments"),
                create_category_card("Medicines", ft.Icons.MEDICATION_ROUNDED, "medicines"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            ft.Row([
                create_category_card("Lab Tests", ft.Icons.SCIENCE_ROUNDED, "scan_lab"),
                create_category_card("Reports", ft.Icons.ASSIGNMENT_ROUNDED, "reports"),
                create_category_card("More", ft.Icons.GRID_VIEW_ROUNDED, "risk_ml"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ], spacing=10),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 6. "Top Doctors" Section with Quick Preview Cards
    doctors_header = ft.Container(
        content=ft.Row([
            ft.Text("Top Doctors", size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.TextButton("See All", on_click=lambda _: navigate_to("doctors"))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=2)
    )

    def create_preview_doctor_card(name: str, specialty: str, rating: str, img_src: str):
        return ft.Container(
            content=ft.Row([
                ft.Image(src=img_src, width=54, height=54, fit=ft.BoxFit.COVER, border_radius=14),
                ft.Column([
                    ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text(specialty, size=11, color="#64748B"),
                    ft.Row([
                        ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color="#F59E0B"),
                        ft.Text(rating, size=11, weight=ft.FontWeight.BOLD, color="#0F172A"),
                        ft.Container(width=4),
                        ft.Container(
                            content=ft.Text("Available", size=9, weight=ft.FontWeight.BOLD, color="#16A34A"),
                            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                            border_radius=6,
                            bgcolor="#DCFCE7"
                        )
                    ], spacing=2)
                ], expand=True, spacing=2),
                ft.Container(
                    content=ft.Text("Book", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=6),
                    border_radius=12,
                    bgcolor="#2563EB",
                    ink=True,
                    on_click=lambda _: navigate_to("profile")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            padding=12,
            border_radius=18,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000")),
            margin=ft.Padding.symmetric(horizontal=18, vertical=4),
            ink=True,
            on_click=lambda _: navigate_to("profile")
        )

    # Scrollable Assembly
    return ft.ListView(
        controls=[
            status_bar,
            header_section,
            search_bar,
            consult_banner,
            categories_grid,
            doctors_header,
            create_preview_doctor_card("Dr. Rohan Mehta", "General Physician", "4.8", DOCTOR_MALE_1),
            create_preview_doctor_card("Dr. Ananya Sharma", "Cardiologist", "4.9", DOCTOR_FEMALE),
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
