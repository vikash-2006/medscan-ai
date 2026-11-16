import flet as ft
from app.state import state

# Path to generated high-res image assets
ROBOT_IMG = "/Users/apple/MedScan AI/app/assets/robot_avatar.jpg"
DOCTOR_IMG = "/Users/apple/MedScan AI/app/assets/doctor_portrait.jpg"

def build_aura_home_screen(page: ft.Page, navigate_to) -> ft.Control:
    # -------------------------------------------------------------
    # 1. Top Status Bar Mockup (10:24, Wifi, Battery)
    # -------------------------------------------------------------
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("10:24", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color=ft.Colors.BLACK87),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color=ft.Colors.BLACK87),
                ft.Container(
                    content=ft.Row([
                        ft.Text("100", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
                        ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=15, color=ft.Colors.BLACK87),
                    ], spacing=2)
                )
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=18, vertical=4)
    )

    # -------------------------------------------------------------
    # 2. Main App Header (Menu, AURA MEDICAL Logo, Bell)
    # -------------------------------------------------------------
    app_header = ft.Container(
        content=ft.Row([
            # Left Hamburger Button
            ft.Container(
                content=ft.Icon(ft.Icons.MENU_ROUNDED, color=ft.Colors.BLUE_GREY_800, size=20),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.WHITE,
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
                alignment=ft.alignment.center
            ),
            # Center Brand Title
            ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.HEALTH_AND_SAFETY_ROUNDED, color=ft.Colors.TEAL_600, size=24),
                    padding=ft.padding.only(right=4)
                ),
                ft.Column([
                    ft.Row([
                        ft.Text("AURA ", size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                        ft.Text("MEDICAL", size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_700),
                    ], spacing=0),
                    ft.Text("AI Health Assistant", size=11, color=ft.Colors.GREY_600, weight=ft.FontWeight.W_500),
                ], spacing=0, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=2),
            # Right Notification Bell with red dot
            ft.Stack([
                ft.Container(
                    content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=ft.Colors.BLUE_GREY_800, size=20),
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
                    alignment=ft.alignment.center
                ),
                ft.Container(
                    width=9,
                    height=9,
                    border_radius=4.5,
                    bgcolor=ft.Colors.RED_ACCENT,
                    top=2,
                    right=2,
                    border=ft.border.all(1.5, ft.Colors.WHITE)
                )
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=6)
    )

    # -------------------------------------------------------------
    # 3. Hero Section: 3D Robot Doctor + Greeting
    # -------------------------------------------------------------
    hero_section = ft.Container(
        content=ft.Row([
            # 3D Robot Avatar
            ft.Container(
                content=ft.Image(
                    src=ROBOT_IMG,
                    width=100,
                    height=100,
                    fit=ft.ImageFit.CONTAIN,
                    border_radius=20
                ),
                width=105,
                height=105,
                alignment=ft.alignment.center
            ),
            # Greeting Text
            ft.Column([
                ft.Text("Hi Vikash! 👋", size=20, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text("I'm AURA, your AI Medical Assistant.", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_800),
                ft.Text(
                    "Tell me your symptoms, get health advice, find doctors, or manage your care.",
                    size=11,
                    color=ft.Colors.BLUE_GREY_600
                ),
            ], expand=True, spacing=3)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        padding=ft.padding.symmetric(horizontal=16, vertical=8)
    )

    # -------------------------------------------------------------
    # 4. Interactive Voice Waveform & Glowing Mic Section
    # -------------------------------------------------------------
    def create_waveform_bar(height):
        return ft.Container(
            width=3.5,
            height=height,
            border_radius=2,
            bgcolor=ft.Colors.CYAN_300
        )

    left_wave = ft.Row([
        create_waveform_bar(4),
        create_waveform_bar(7),
        create_waveform_bar(12),
        create_waveform_bar(18),
        create_waveform_bar(24),
        create_waveform_bar(16),
        create_waveform_bar(10),
        create_waveform_bar(5),
    ], spacing=3, alignment=ft.MainAxisAlignment.CENTER)

    right_wave = ft.Row([
        create_waveform_bar(5),
        create_waveform_bar(10),
        create_waveform_bar(16),
        create_waveform_bar(24),
        create_waveform_bar(18),
        create_waveform_bar(12),
        create_waveform_bar(7),
        create_waveform_bar(4),
    ], spacing=3, alignment=ft.MainAxisAlignment.CENTER)

    # Center Glowing Mic
    mic_button = ft.Container(
        content=ft.Icon(ft.Icons.MIC_ROUNDED, color=ft.Colors.WHITE, size=32),
        width=74,
        height=74,
        border_radius=37,
        gradient=ft.RadialGradient(
            colors=[ft.Colors.CYAN_400, ft.Colors.TEAL_600],
            center=ft.alignment.center
        ),
        shadow=ft.BoxShadow(spread_radius=3, blur_radius=18, color=ft.Colors.CYAN_200),
        alignment=ft.alignment.center,
        ink=True,
        on_click=lambda _: toggle_mic_state()
    )

    tap_to_speak_pill = ft.Container(
        content=ft.Text("Tap to speak", size=12, weight=ft.FontWeight.W_500, color=ft.Colors.BLUE_GREY_700),
        padding=ft.padding.symmetric(horizontal=14, vertical=5),
        border_radius=14,
        bgcolor=ft.Colors.WHITE,
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=ft.Colors.BLACK12)
    )

    # State Chips (Listening, Thinking, Speaking)
    listening_chip = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.GRAPHIC_EQ_ROUNDED, size=15, color=ft.Colors.TEAL_700),
            ft.Text("Listening", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.TEAL_800),
        ], spacing=4),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=ft.Colors.TEAL_50,
        border=ft.border.all(1, ft.Colors.TEAL_400)
    )

    thinking_chip = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.DONUT_LARGE_ROUNDED, size=14, color=ft.Colors.GREY_600),
            ft.Text("Thinking", size=11, color=ft.Colors.GREY_700),
        ], spacing=4),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=ft.Colors.GREY_100
    )

    speaking_chip = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.VOLUME_UP_ROUNDED, size=14, color=ft.Colors.GREY_600),
            ft.Text("Speaking", size=11, color=ft.Colors.GREY_700),
        ], spacing=4),
        padding=ft.padding.symmetric(horizontal=12, vertical=6),
        border_radius=16,
        bgcolor=ft.Colors.GREY_100
    )

    voice_section = ft.Container(
        content=ft.Column([
            ft.Row([
                left_wave,
                ft.Container(content=mic_button, padding=ft.padding.symmetric(horizontal=12)),
                right_wave
            ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.CENTER),
            ft.Container(content=tap_to_speak_pill, alignment=ft.alignment.center),
            ft.Row([
                listening_chip,
                thinking_chip,
                speaking_chip
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=10)
        ], spacing=8, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=ft.padding.symmetric(vertical=8)
    )

    # -------------------------------------------------------------
    # 5. Conversational Chat Stream
    # -------------------------------------------------------------
    chat_list = ft.Column(spacing=10)

    # Sample User Bubble
    user_bubble = ft.Row([
        ft.Container(
            content=ft.Column([
                ft.Text("I have a stomach pain since last night. What should I do?", size=13, color=ft.Colors.BLUE_GREY_900),
                ft.Row([
                    ft.Text("10:24 AM", size=10, color=ft.Colors.BLUE_GREY_500),
                    ft.Icon(ft.Icons.DONE_ALL_ROUNDED, size=13, color=ft.Colors.BLUE_600)
                ], alignment=ft.MainAxisAlignment.END, spacing=2)
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=ft.border_radius.only(top_left=16, top_right=4, bottom_left=16, bottom_right=16),
            bgcolor="#E0EFFF",
            width=270
        ),
        ft.CircleAvatar(
            content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=18),
            bgcolor=ft.Colors.BLUE_500,
            radius=16
        )
    ], alignment=ft.MainAxisAlignment.END, vertical_alignment=ft.CrossAxisAlignment.START, spacing=8)

    # Sample Assistant Bubble
    assistant_bubble = ft.Row([
        ft.Container(
            content=ft.Image(src=ROBOT_IMG, width=32, height=32, fit=ft.ImageFit.COVER, border_radius=16),
            width=32,
            height=32
        ),
        ft.Container(
            content=ft.Column([
                ft.Text(
                    "Stomach pain can happen due to indigestion, acidity, or infection. Let me ask a few quick questions to understand better.",
                    size=13,
                    color=ft.Colors.BLUE_GREY_900
                ),
                ft.Text("10:24 AM", size=10, color=ft.Colors.GREY_500)
            ], spacing=2),
            padding=ft.padding.symmetric(horizontal=14, vertical=10),
            border_radius=ft.border_radius.only(top_left=4, top_right=16, bottom_left=16, bottom_right=16),
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.BLUE_GREY_50),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
            width=270
        )
    ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.START, spacing=8)

    chat_list.controls.extend([user_bubble, assistant_bubble])

    # -------------------------------------------------------------
    # 6. Interactive Symptom Follow-Up Chips
    # -------------------------------------------------------------
    def send_chip_query(query_text: str):
        # Add user query to chat
        chat_list.controls.append(
            ft.Row([
                ft.Container(
                    content=ft.Text(query_text, size=13, color=ft.Colors.BLUE_GREY_900),
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    border_radius=ft.border_radius.only(top_left=16, top_right=4, bottom_left=16, bottom_right=16),
                    bgcolor="#E0EFFF",
                ),
                ft.CircleAvatar(content=ft.Icon(ft.Icons.PERSON, color=ft.Colors.WHITE, size=18), bgcolor=ft.Colors.BLUE_500, radius=16)
            ], alignment=ft.MainAxisAlignment.END, spacing=8)
        )
        
        # Add bot answer
        reply = "Agar pain sharp ya continuous hai aur vomiting/fever ke sath hai toh immediately Sanjeevani Risk Checkup run karein ya doctor se consult karein."
        chat_list.controls.append(
            ft.Row([
                ft.Container(content=ft.Image(src=ROBOT_IMG, width=32, height=32, fit=ft.ImageFit.COVER, border_radius=16), width=32, height=32),
                ft.Container(
                    content=ft.Text(reply, size=13, color=ft.Colors.BLUE_GREY_900),
                    padding=ft.padding.symmetric(horizontal=14, vertical=10),
                    border_radius=ft.border_radius.only(top_left=4, top_right=16, bottom_left=16, bottom_right=16),
                    bgcolor=ft.Colors.WHITE,
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
                    width=270
                )
            ], alignment=ft.MainAxisAlignment.START, spacing=8)
        )
        page.update()

    def toggle_mic_state():
        send_chip_query("Can you analyze my recent blood test report?")

    chips_row = ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ASSIGNMENT_OUTLINED, color=ft.Colors.TEAL_700, size=16),
                ft.Text("How severe is the pain?", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.TEAL_900),
            ], spacing=6),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=18,
            border=ft.border.all(1, ft.Colors.TEAL_200),
            bgcolor=ft.Colors.WHITE,
            ink=True,
            on_click=lambda _: send_chip_query("How severe is the pain?")
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.MEDICAL_SERVICES_OUTLINED, color=ft.Colors.TEAL_700, size=16),
                ft.Text("Do you have nausea?", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.TEAL_900),
            ], spacing=6),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=18,
            border=ft.border.all(1, ft.Colors.TEAL_200),
            bgcolor=ft.Colors.WHITE,
            ink=True,
            on_click=lambda _: send_chip_query("Do you have nausea?")
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.EVENT_NOTE_OUTLINED, color=ft.Colors.TEAL_700, size=16),
                ft.Text("Since when is it happening?", size=11, weight=ft.FontWeight.W_500, color=ft.Colors.TEAL_900),
            ], spacing=6),
            padding=ft.padding.symmetric(horizontal=12, vertical=8),
            border_radius=18,
            border=ft.border.all(1, ft.Colors.TEAL_200),
            bgcolor=ft.Colors.WHITE,
            ink=True,
            on_click=lambda _: send_chip_query("Since when is it happening?")
        ),
    ], scroll=ft.ScrollMode.ADAPTIVE, spacing=8)

    # -------------------------------------------------------------
    # 7. 4 Quick Action Feature Cards (Pastel Backgrounds)
    # -------------------------------------------------------------
    def create_feature_card(title, icon_data, bg_color, icon_color, target_tab):
        return ft.Container(
            content=ft.Column([
                ft.Icon(icon_data, color=icon_color, size=28),
                ft.Text(title, size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900, text_align=ft.TextAlign.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            width=82,
            height=88,
            border_radius=16,
            bgcolor=bg_color,
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=ft.Colors.BLACK12),
            ink=True,
            on_click=lambda _: navigate_to(target_tab)
        )

    action_cards_row = ft.Row([
        create_feature_card("Check\nSymptoms", ft.Icons.STETHOSCOPE if hasattr(ft.Icons, "STETHOSCOPE") else ft.Icons.HEALTH_AND_SAFETY_ROUNDED, "#E8F1FF", ft.Colors.BLUE_600, 3),
        create_feature_card("Book\nAppointment", ft.Icons.CALENDAR_MONTH_ROUNDED, "#E8F8F2", ft.Colors.TEAL_600, 0),
        create_feature_card("Medicine\nReminder", ft.Icons.MEDICATION_ROUNDED, "#F3EDFD", ft.Colors.PURPLE_600, 0),
        create_feature_card("Health\nReports", ft.Icons.RECEIPT_LONG_ROUNDED, "#EAF4FF", ft.Colors.LIGHT_BLUE_700, 1),
    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    # -------------------------------------------------------------
    # 8. Doctor Consultation Promo Card
    # -------------------------------------------------------------
    doctor_card = ft.Container(
        content=ft.Row([
            # Doctor Photo
            ft.Container(
                content=ft.Image(
                    src=DOCTOR_IMG,
                    width=78,
                    height=88,
                    fit=ft.ImageFit.COVER,
                    border_radius=16
                ),
                width=82,
                height=92,
                alignment=ft.alignment.center
            ),
            # Text + Badges + Button
            ft.Column([
                ft.Row([
                    ft.Text("Consult a Doctor Online", size=14, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ]),
                ft.Text("Get expert advice from verified doctors within minutes.", size=11, color=ft.Colors.BLUE_GREY_600),
                ft.Container(
                    content=ft.Row([
                        ft.Icon(ft.Icons.VIDEOCAM_ROUNDED, color=ft.Colors.WHITE, size=15),
                        ft.Text("Consult Now >", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    ], spacing=4),
                    padding=ft.padding.symmetric(horizontal=12, vertical=6),
                    border_radius=14,
                    bgcolor=ft.Colors.TEAL_600,
                    ink=True,
                    on_click=lambda _: page.open(ft.SnackBar(ft.Text("Connecting to Doctor consultation network...")))
                ),
                ft.Row([
                    ft.Row([ft.Icon(ft.Icons.CHECK_CIRCLE, size=11, color=ft.Colors.GREEN_600), ft.Text("Verified", size=10, color=ft.Colors.GREY_700)], spacing=2),
                    ft.Row([ft.Icon(ft.Icons.ACCESS_TIME, size=11, color=ft.Colors.TEAL_600), ft.Text("24x7", size=10, color=ft.Colors.GREY_700)], spacing=2),
                    ft.Row([ft.Icon(ft.Icons.FLASH_ON, size=11, color=ft.Colors.AMBER_600), ft.Text("Fast", size=10, color=ft.Colors.GREY_700)], spacing=2),
                ], spacing=8)
            ], expand=True, spacing=4)
        ], alignment=ft.MainAxisAlignment.START, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
        padding=12,
        border_radius=18,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#F0FDF4", "#EFF6FF"]
        ),
        border=ft.border.all(1, ft.Colors.BLUE_GREY_100),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.BLACK12)
    )

    # -------------------------------------------------------------
    # Assemble Screen in Scrollable List
    # -------------------------------------------------------------
    return ft.ListView(
        controls=[
            status_bar,
            app_header,
            hero_section,
            voice_section,
            ft.Container(content=chat_list, padding=ft.padding.symmetric(horizontal=16)),
            ft.Container(height=6),
            ft.Container(content=chips_row, padding=ft.padding.symmetric(horizontal=16)),
            ft.Container(height=10),
            ft.Container(content=action_cards_row, padding=ft.padding.symmetric(horizontal=16)),
            ft.Container(height=10),
            ft.Container(content=doctor_card, padding=ft.padding.symmetric(horizontal=16)),
            ft.Container(height=30)
        ],
        spacing=6,
        padding=0
    )
