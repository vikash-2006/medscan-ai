import os
import flet as ft

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

def build_sanjeevani_splash_screen(page: ft.Page, navigate_to) -> ft.Control:
    # 1. iOS Top Status Bar (9:41, wifi, battery)
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("9:41", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color="#0F172A"),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color="#0F172A"),
                ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=17, color="#0F172A"),
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=24, vertical=8)
    )

    # 2. Glowing Medical Cross Icon with Heartbeat Wave
    medical_logo = ft.Container(
        content=ft.Stack([
            # Outer soft aura glow
            ft.Container(
                width=110,
                height=110,
                border_radius=55,
                bgcolor="#EAF4FF",
                alignment=ft.Alignment.CENTER,
            ),
            # Inner Royal Blue Icon Badge
            ft.Container(
                content=ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED, size=52, color=ft.Colors.WHITE),
                width=86,
                height=86,
                border_radius=43,
                bgcolor="#2563EB",
                alignment=ft.Alignment.CENTER,
                shadow=ft.BoxShadow(
                    spread_radius=2,
                    blur_radius=24,
                    color=ft.Colors.with_opacity(0.35, "#2563EB")
                )
            ),
        ], alignment=ft.Alignment.CENTER),
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.only(top=40, bottom=16)
    )

    # 3. Typography: "Sanjeevani Healthcare"
    brand_title = ft.Column([
        ft.Text(
            "Sanjeevani",
            size=34,
            weight=ft.FontWeight.BOLD,
            color="#0F172A",
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            "Healthcare",
            size=18,
            weight=ft.FontWeight.W_500,
            color="#64748B",
            text_align=ft.TextAlign.CENTER,
        ),
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2)

    # 4. Cardiogram Pulse Wave Graphic
    cardiogram_line = ft.Container(
        content=ft.Row([
            ft.Container(width=40, height=2, bgcolor="#93C5FD"),
            ft.Icon(ft.Icons.SHOW_CHART_ROUNDED, size=32, color="#2563EB"),
            ft.Container(width=40, height=2, bgcolor="#93C5FD"),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
        padding=ft.Padding.symmetric(vertical=24)
    )

    # 5. Bottom Fluid Decorative Wave & "Get Started" CTA Button
    get_started_btn = ft.Container(
        content=ft.Row([
            ft.Text("Get Started", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
            ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=18, color=ft.Colors.WHITE),
        ], alignment=ft.MainAxisAlignment.CENTER, spacing=8),
        width=320,
        height=54,
        border_radius=27,
        bgcolor="#2563EB",
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=18,
            color=ft.Colors.with_opacity(0.35, "#2563EB")
        ),
        ink=True,
        on_click=lambda _: navigate_to("home")
    )

    bottom_wave_section = ft.Container(
        content=ft.Column([
            get_started_btn,
            ft.Container(height=16),
            ft.Text("AI-Powered Clinical Diagnostics & Consultation", size=11, color="#94A3B8")
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.only(bottom=40),
        alignment=ft.Alignment.CENTER
    )

    return ft.Container(
        content=ft.Column([
            status_bar,
            ft.Container(
                content=ft.Column([
                    medical_logo,
                    brand_title,
                    cardiogram_line,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                expand=True,
                alignment=ft.Alignment.CENTER
            ),
            bottom_wave_section
        ], expand=True, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        expand=True,
        bgcolor="#F8FAFC"
    )
