import os
import flet as ft

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_ROHAN = _get_asset("doctor_portrait.jpg")
ROBOT_IMG = _get_asset("robot_avatar.jpg")

def build_sanjeevani_video_screen(page: ft.Page, navigate_to) -> ft.Control:
    # Top overlay with back arrow and call duration
    top_overlay = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color=ft.Colors.WHITE, size=18),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: navigate_to("appointments")
            ),
            ft.Container(
                content=ft.Row([
                    ft.Container(width=8, height=8, border_radius=4, bgcolor="#22C55E"),
                    ft.Text("Live Consultation • 12:45", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                ], spacing=6),
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border_radius=14,
                bgcolor=ft.Colors.with_opacity(0.4, "#000000")
            ),
            ft.Container(
                content=ft.Icon(ft.Icons.MORE_VERT_ROUNDED, color=ft.Colors.WHITE, size=20),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                alignment=ft.Alignment.CENTER
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=12)
    )

    # Doctor stream view (simulated with portrait image)
    doctor_feed = ft.Container(
        content=ft.Stack([
            ft.Image(
                src=DOCTOR_ROHAN,
                width=360,
                height=520,
                fit=ft.BoxFit.COVER,
                border_radius=28
            ),
            # Doctor Name Badge overlay on stream
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.VERIFIED_ROUNDED, color="#2563EB", size=16),
                    ft.Text("Dr. Rohan Mehta", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ft.Text("• General Physician", size=11, color=ft.Colors.WHITE70)
                ], spacing=4),
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                border_radius=12,
                bgcolor=ft.Colors.with_opacity(0.65, "#0F172A"),
                bottom=16,
                left=16
            ),
            # Patient PIP preview in top-right corner
            ft.Container(
                content=ft.Image(
                    src=ROBOT_IMG,
                    width=75,
                    height=95,
                    fit=ft.BoxFit.COVER,
                    border_radius=14
                ),
                width=75,
                height=95,
                border_radius=14,
                border=ft.Border.all(2, ft.Colors.WHITE),
                top=16,
                right=16,
                shadow=ft.BoxShadow(spread_radius=1, blur_radius=8, color=ft.Colors.BLACK38)
            )
        ]),
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.symmetric(horizontal=14)
    )

    # Call controls bottom bar (Mute, Camera toggle, Chat, End call)
    def create_call_btn(icon_data, bg_color, is_end: bool = False, on_click=None):
        return ft.Container(
            content=ft.Icon(icon_data, color=ft.Colors.WHITE, size=22),
            width=54,
            height=54,
            border_radius=27,
            bgcolor=bg_color,
            alignment=ft.Alignment.CENTER,
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=10, color=ft.Colors.BLACK26),
            ink=True,
            on_click=on_click
        )

    controls_bar = ft.Container(
        content=ft.Row([
            create_call_btn(ft.Icons.MIC_ROUNDED, "#334155"),
            create_call_btn(ft.Icons.VIDEOCAM_ROUNDED, "#334155"),
            create_call_btn(ft.Icons.CHAT_BUBBLE_ROUNDED, "#334155", on_click=lambda _: page.open(ft.SnackBar(ft.Text("Opening prescription notes...")))),
            create_call_btn(ft.Icons.CALL_END_ROUNDED, "#EF4444", is_end=True, on_click=lambda _: navigate_to("appointments")),
        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
        border_radius=32,
        bgcolor="#0F172A",
        margin=ft.Padding.symmetric(horizontal=18, vertical=10)
    )

    return ft.Container(
        content=ft.Column([
            top_overlay,
            ft.Container(content=doctor_feed, expand=True, alignment=ft.Alignment.CENTER),
            controls_bar
        ], expand=True),
        expand=True,
        bgcolor="#0B132B"
    )
