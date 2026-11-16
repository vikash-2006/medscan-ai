import os
import flet as ft
from app.state import state

# Dynamic asset resolution for Desktop, Web, and Android APK
_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_FEMALE_IMG = _get_asset("doctor_female.jpg")
DOCTOR_MALE_IMG = _get_asset("doctor_portrait.jpg")

def build_android_consult_screen(page: ft.Page, navigate_to) -> ft.Control:
    # Top Status Bar
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("9:41", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK_87),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color=ft.Colors.BLACK_87),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color=ft.Colors.BLACK_87),
                ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=16, color=ft.Colors.BLACK_87),
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=16, vertical=4)
    )

    # Screen Title Header
    title_section = ft.Container(
        content=ft.Column([
            ft.Text("Book Doctor", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Text("Visits in Minutes", size=24, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.Container(height=6),
            # Medical Clipboard badge illustration
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.ASSIGNMENT_TURNED_IN_ROUNDED, size=28, color=ft.Colors.BLUE_600),
                    ft.Icon(ft.Icons.ADD_CIRCLE_ROUNDED, size=22, color=ft.Colors.PINK_400),
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=-6),
                alignment=ft.Alignment.CENTER
            )
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
        padding=ft.Padding.symmetric(vertical=10),
        alignment=ft.Alignment.CENTER
    )

    # Chat Messages Stream Container
    chat_column = ft.Column(spacing=8)

    # Sample preloaded messages matching the left phone mock
    msg_received = ft.Row([
        ft.Container(
            content=ft.Text(
                "Hello Vikash, how are you feeling today? Any chest discomfort or shortness of breath?",
                size=12,
                color=ft.Colors.BLUE_GREY_900
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=ft.BorderRadius.only(top_left=4, top_right=16, bottom_left=16, bottom_right=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, ft.Colors.GREY_200),
            width=250
        )
    ], alignment=ft.MainAxisAlignment.START)

    msg_sent = ft.Row([
        ft.Container(
            content=ft.Text(
                "I had mild dizziness and my fasting blood sugar was 158 mg/dL this morning.",
                size=12,
                color=ft.Colors.BLUE_900
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=10),
            border_radius=ft.BorderRadius.only(top_left=16, top_right=4, bottom_left=16, bottom_right=16),
            bgcolor="#BFDBFE",  # Soft pastel blue
            width=250
        )
    ], alignment=ft.MainAxisAlignment.END)

    chat_column.controls.extend([msg_received, msg_sent])

    # Message input field
    msg_input = ft.TextField(
        hint_text="Type something...",
        dense=True,
        border=ft.InputBorder.NONE,
        text_size=12,
        expand=True
    )

    def send_message(e):
        txt = msg_input.value.strip()
        if not txt:
            return
        
        chat_column.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(txt, size=12, color=ft.Colors.BLUE_900),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    border_radius=ft.BorderRadius.only(top_left=16, top_right=4, bottom_left=16, bottom_right=16),
                    bgcolor="#BFDBFE",
                    width=250
                )
            ], alignment=ft.MainAxisAlignment.END)
        )
        msg_input.value = ""
        page.update()

        # Doctor auto-reply
        reply = "Noted. I recommend uploading your full lipid report in 'Scan Lab' or running the Sanjeevani Risk Triage."
        chat_column.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(reply, size=12, color=ft.Colors.BLUE_GREY_900),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    border_radius=ft.BorderRadius.only(top_left=4, top_right=16, bottom_left=16, bottom_right=16),
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, ft.Colors.GREY_200),
                    width=250
                )
            ], alignment=ft.MainAxisAlignment.START)
        )
        page.update()

    # Floating Card wrapping doctor info, chat, and input
    chat_card = ft.Container(
        content=ft.Column([
            # Doctor Header Row
            ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Image(
                            src=DOCTOR_FEMALE_IMG,
                            width=38,
                            height=38,
                            fit=ft.BoxFit.COVER,
                            border_radius=19
                        ),
                        width=38,
                        height=38
                    ),
                    ft.Column([
                        ft.Text("Dr. Olivia Nelson", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                        ft.Text("Online Specialist", size=10, color=ft.Colors.GREY_500),
                    ], spacing=1)
                ], spacing=8),
                # Online Dot
                ft.Container(
                    width=9,
                    height=9,
                    border_radius=4.5,
                    bgcolor=ft.Colors.BLUE_600
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Divider(height=12, color=ft.Colors.GREY_200),

            # Chat Stream
            chat_column,

            ft.Container(height=8),

            # Input Composer Box
            ft.Container(
                content=ft.Row([
                    msg_input,
                    ft.IconButton(
                        icon=ft.Icons.ATTACH_FILE_ROUNDED,
                        icon_size=18,
                        icon_color=ft.Colors.GREY_500,
                        on_click=lambda _: navigate_to(2)
                    ),
                    ft.IconButton(
                        icon=ft.Icons.SEND_ROUNDED,
                        icon_size=18,
                        icon_color=ft.Colors.BLUE_600,
                        on_click=send_message
                    )
                ], spacing=0),
                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                border_radius=16,
                border=ft.Border.all(1, ft.Colors.GREY_300),
                bgcolor=ft.Colors.WHITE
            )
        ], spacing=6),
        padding=16,
        border_radius=24,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.BLUE_50),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=16, color=ft.Colors.BLUE_100),
        margin=ft.Padding.symmetric(horizontal=16, vertical=6)
    )

    # Bottom Swipe/Stethoscope action pill matching the left phone mock
    bottom_action_pill = ft.Container(
        content=ft.Column([
            ft.Container(
                content=ft.Icon(ft.Icons.LOCAL_HOSPITAL_ROUNDED, size=24, color=ft.Colors.WHITE),
                width=50,
                height=50,
                border_radius=25,
                bgcolor=ft.Colors.BLUE_800,
                alignment=ft.Alignment.CENTER
            ),
            ft.Icon(ft.Icons.KEYBOARD_DOUBLE_ARROW_DOWN_ROUNDED, size=18, color=ft.Colors.BLUE_800),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=4),
        alignment=ft.Alignment.CENTER,
        padding=ft.Padding.only(top=10)
    )

    return ft.ListView(
        controls=[
            status_bar,
            title_section,
            chat_card,
            bottom_action_pill,
            ft.Container(height=40)
        ],
        spacing=6,
        padding=0
    )
