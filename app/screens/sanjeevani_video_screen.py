import os
import flet as ft
from app.state import state
from app.utils import show_snackbar, show_dialog_modal

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTOR_IMG = _get_asset("doctor_portrait.jpg")
PATIENT_IMG = _get_asset("robot_avatar.jpg")

def build_sanjeevani_video_screen(page: ft.Page, navigate_to) -> ft.Control:
    # Get active doctor name
    active_appt = state.booked_appointments[0] if state.booked_appointments else {}
    doc_name = active_appt.get("doctor_name", "Dr. Rohan Mehta")

    # Interactive call states
    mic_muted = False
    camera_off = False

    mic_icon = ft.Icon(ft.Icons.MIC_ROUNDED, color=ft.Colors.WHITE, size=24)
    camera_icon = ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, color=ft.Colors.WHITE, size=24)
    mic_btn_container = ft.Container()
    cam_btn_container = ft.Container()

    def toggle_mic(e):
        nonlocal mic_muted
        mic_muted = not mic_muted
        mic_icon.name = ft.Icons.MIC_OFF_ROUNDED if mic_muted else ft.Icons.MIC_ROUNDED
        mic_btn.bgcolor = "#EF4444" if mic_muted else "#334155"
        show_snackbar(page, "Microphone Muted" if mic_muted else "Microphone Unmuted", bgcolor="#EF4444" if mic_muted else "#2563EB")
        page.update()

    def toggle_cam(e):
        nonlocal camera_off
        camera_off = not camera_off
        camera_icon.name = ft.Icons.VIDEOCAM_OFF_ROUNDED if camera_off else ft.Icons.VIDEOCAM_ROUNDED
        cam_btn.bgcolor = "#EF4444" if camera_off else "#334155"
        pip_video.visible = not camera_off
        show_snackbar(page, "Camera Paused" if camera_off else "Camera Active", bgcolor="#EF4444" if camera_off else "#2563EB")
        page.update()

    def end_call(e):
        show_snackbar(page, f"Consultation with {doc_name} concluded successfully.", bgcolor="#16A34A")
        navigate_to("appointments")

    def show_prescription(e):
        note_content = ft.Column([
            ft.Text("Prescription & Doctor Advisory Notes", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Text(f"Doctor: {doc_name}\nPatient: {state.patient_name}", size=12, color="#64748B"),
            ft.Container(height=4),
            ft.Text("Rx Recommendations:\n1. Tab Metformin 500mg (1-0-1 post meals)\n2. Maintain daily blood sugar log\n3. Reduce simple carbs and 30min brisk walk",
                    size=12, color="#334155", line_height=1.4),
        ], spacing=4)
        show_dialog_modal(page, "Consultation Notes", note_content)

    # 1. Top Call Header (Back, Doctor Name, Duration timer)
    top_bar = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color=ft.Colors.WHITE, size=18),
                width=40,
                height=40,
                border_radius=20,
                bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: navigate_to("appointments")
            ),
            ft.Column([
                ft.Text(doc_name, size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                ft.Row([
                    ft.Container(width=6, height=6, border_radius=3, bgcolor="#22C55E"),
                    ft.Text("Live Consultation • 04:18", size=11, color="#86EFAC")
                ], spacing=4)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
            ft.Container(
                content=ft.Icon(ft.Icons.NOTE_ALT_OUTLINED, color=ft.Colors.WHITE, size=18),
                width=40,
                height=40,
                border_radius=20,
                bgcolor=ft.Colors.with_opacity(0.3, "#000000"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=show_prescription
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=12)
    )

    # 2. Main Video Feed (Doctor Stream)
    main_video = ft.Container(
        content=ft.Image(
            src=DOCTOR_IMG,
            fit=ft.BoxFit.COVER,
            expand=True
        ),
        expand=True,
        border_radius=24,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        margin=ft.Padding.symmetric(horizontal=12, vertical=6)
    )

    # 3. Patient Picture-in-Picture (PIP) Window
    pip_video = ft.Container(
        content=ft.Image(
            src=PATIENT_IMG,
            width=90,
            height=130,
            fit=ft.BoxFit.COVER,
            border_radius=16
        ),
        width=90,
        height=130,
        border_radius=16,
        border=ft.Border.all(2, ft.Colors.WHITE),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color=ft.Colors.BLACK45),
        right=24,
        top=80
    )

    # 4. Bottom Controls Bar
    mic_btn = ft.Container(
        content=mic_icon,
        width=54,
        height=54,
        border_radius=27,
        bgcolor="#334155",
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=toggle_mic
    )

    cam_btn = ft.Container(
        content=camera_icon,
        width=54,
        height=54,
        border_radius=27,
        bgcolor="#334155",
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=toggle_cam
    )

    end_btn = ft.Container(
        content=ft.Icon(ft.Icons.CALL_END_ROUNDED, color=ft.Colors.WHITE, size=28),
        width=60,
        height=60,
        border_radius=30,
        bgcolor="#EF4444",
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=end_call
    )

    notes_btn = ft.Container(
        content=ft.Icon(ft.Icons.CHAT_BUBBLE_ROUNDED, color=ft.Colors.WHITE, size=22),
        width=54,
        height=54,
        border_radius=27,
        bgcolor="#334155",
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=show_prescription
    )

    controls_bar = ft.Container(
        content=ft.Row([
            mic_btn,
            cam_btn,
            end_btn,
            notes_btn
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY, vertical_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.Padding.symmetric(vertical=20),
        bgcolor=ft.Colors.with_opacity(0.85, "#0F172A"),
        border_radius=ft.BorderRadius.only(top_left=28, top_right=28)
    )

    # Complete Screen Wrapped in dark container
    return ft.Container(
        content=ft.Stack([
            ft.Column([
                top_bar,
                main_video,
                controls_bar
            ], expand=True, spacing=0),
            pip_video
        ]),
        expand=True,
        bgcolor="#0B132B"
    )
