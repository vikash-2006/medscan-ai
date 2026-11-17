import os
import flet as ft

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_ROHAN = _get_asset("doctor_portrait.jpg")
DOCTOR_ANANYA = _get_asset("doctor_female.jpg")
DOCTOR_VIVEK = _get_asset("doctor_male_2.jpg")

def build_sanjeevani_doctors_screen(page: ft.Page, navigate_to) -> ft.Control:
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

    # 2. Header with Back Button and Title
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
                on_click=lambda _: navigate_to("home")
            ),
            ft.Text("Doctors", size=18, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(
                content=ft.Icon(ft.Icons.SEARCH_ROUNDED, color="#0F172A", size=20),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: None
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 3. Horizontal Category Filter Chips
    selected_filter = "All"

    def create_filter_chip(label: str, is_active: bool = False):
        if is_active:
            return ft.Container(
                content=ft.Text(label, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                border_radius=20,
                bgcolor="#2563EB",
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.25, "#2563EB")),
                ink=True
            )
        else:
            return ft.Container(
                content=ft.Text(label, size=12, weight=ft.FontWeight.W_500, color="#64748B"),
                padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                ink=True
            )

    filter_row = ft.Container(
        content=ft.Row([
            create_filter_chip("All", True),
            create_filter_chip("General", False),
            create_filter_chip("Cardiology", False),
            create_filter_chip("Dermatology", False),
        ], spacing=8),
        padding=ft.Padding.symmetric(horizontal=18, vertical=8)
    )

    # 4. Doctor Cards Matching Mockup Phone 3
    def create_doctor_list_card(name: str, specialty: str, rating: str, reviews: str,
                                availability: str, is_today: bool, img_src: str):
        badge_bg = "#DCFCE7" if is_today else "#FEF3C7"
        badge_color = "#16A34A" if is_today else "#D97706"

        return ft.Container(
            content=ft.Column([
                ft.Row([
                    # Doctor Image with smooth rounded frame
                    ft.Image(
                        src=img_src,
                        width=64,
                        height=64,
                        fit=ft.BoxFit.COVER,
                        border_radius=16
                    ),
                    # Doctor Details
                    ft.Column([
                        ft.Text(name, size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                        ft.Text(specialty, size=11, color="#64748B"),
                        ft.Row([
                            ft.Icon(ft.Icons.STAR_ROUNDED, size=15, color="#F59E0B"),
                            ft.Text(rating, size=11, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Text(f"({reviews})", size=10, color="#94A3B8"),
                        ], spacing=3),
                        ft.Row([
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=6, height=6, border_radius=3, bgcolor=badge_color),
                                    ft.Text(availability, size=10, weight=ft.FontWeight.W_600, color=badge_color)
                                ], spacing=4),
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                border_radius=6,
                                bgcolor=badge_bg
                            )
                        ])
                    ], spacing=3, expand=True),

                    # Heart Favorite Icon & "Book" Button
                    ft.Column([
                        ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, color="#94A3B8", size=18),
                        ft.Container(height=12),
                        ft.Container(
                            content=ft.Text("Book", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                            padding=ft.Padding.symmetric(horizontal=18, vertical=8),
                            border_radius=14,
                            bgcolor="#2563EB",
                            ink=True,
                            on_click=lambda _: navigate_to("profile")
                        )
                    ], horizontal_alignment=ft.CrossAxisAlignment.END)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
            ]),
            padding=14,
            border_radius=20,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000")),
            margin=ft.Padding.symmetric(horizontal=18, vertical=5),
            ink=True,
            on_click=lambda _: navigate_to("profile")
        )

    doctors_list = ft.Column([
        create_doctor_list_card("Dr. Rohan Mehta", "General Physician", "4.8", "1,240", "Available Today", True, DOCTOR_ROHAN),
        create_doctor_list_card("Dr. Ananya Sharma", "Cardiologist", "4.9", "980", "Available Today", True, DOCTOR_ANANYA),
        create_doctor_list_card("Dr. Vivek Singh", "Gastroenterologist", "4.7", "750", "Available Tomorrow", False, DOCTOR_VIVEK),
    ], spacing=4)

    return ft.ListView(
        controls=[
            status_bar,
            header,
            filter_row,
            doctors_list,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
