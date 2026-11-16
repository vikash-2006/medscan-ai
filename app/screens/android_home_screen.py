import flet as ft
from app.state import state

DOCTOR_MALE_IMG = "/Users/apple/MedScan AI/app/assets/doctor_portrait.jpg"
DOCTOR_FEMALE_IMG = "/Users/apple/MedScan AI/app/assets/doctor_female.jpg"
ROBOT_IMG = "/Users/apple/MedScan AI/app/assets/robot_avatar.jpg"

def build_android_home_screen(page: ft.Page, navigate_to) -> ft.Control:
    # -------------------------------------------------------------
    # 1. Top Status Bar (9:41, wifi, battery)
    # -------------------------------------------------------------
    status_bar = ft.Container(
        content=ft.Row([
            ft.Text("9:41", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLACK87),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color=ft.Colors.BLACK87),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color=ft.Colors.BLACK87),
                ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=16, color=ft.Colors.BLACK87),
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=4)
    )

    # -------------------------------------------------------------
    # 2. Header (Profile Avatar, "Hello, Vikash", Bell)
    # -------------------------------------------------------------
    header_section = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Container(
                    content=ft.Image(
                        src=DOCTOR_MALE_IMG,
                        width=44,
                        height=44,
                        fit=ft.ImageFit.COVER,
                        border_radius=22
                    ),
                    width=44,
                    height=44,
                ),
                ft.Column([
                    ft.Text("Welcome back", size=11, color=ft.Colors.GREY_600),
                    ft.Text("Hello, Vikash 👋", size=17, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ], spacing=1)
            ], spacing=10),
            
            # Notification Bell Icon
            ft.Container(
                content=ft.Icon(ft.Icons.NOTIFICATIONS_OUTLINED, color=ft.Colors.BLUE_GREY_800, size=22),
                width=40,
                height=40,
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                border=ft.border.all(1, ft.Colors.GREY_200),
                alignment=ft.alignment.center,
                ink=True,
                on_click=lambda _: page.open(ft.SnackBar(ft.Text("Sanjeevani AI Diagnostic System is active!")))
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=8)
    )

    # -------------------------------------------------------------
    # 3. Search Bar
    # -------------------------------------------------------------
    search_bar = ft.Container(
        content=ft.TextField(
            hint_text="Search doctors, lab reports, symptoms...",
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            dense=True,
            border=ft.InputBorder.NONE,
            text_size=13,
            content_padding=ft.padding.symmetric(horizontal=12, vertical=10)
        ),
        bgcolor=ft.Colors.WHITE,
        border_radius=16,
        border=ft.border.all(1, ft.Colors.GREY_200),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
        margin=ft.padding.symmetric(horizontal=16, vertical=4)
    )

    # -------------------------------------------------------------
    # 4. "Your Appointment" Vibrant Deep Blue Card
    # -------------------------------------------------------------
    appointment_header = ft.Container(
        content=ft.Row([
            ft.Text("Your Appointment", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.TextButton("See Details", on_click=lambda _: navigate_to(1))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=2)
    )

    appointment_card = ft.Container(
        content=ft.Column([
            # Top row: Doctor Info + "4 Days" badge
            ft.Row([
                ft.Row([
                    ft.Container(
                        content=ft.Image(
                            src=DOCTOR_MALE_IMG,
                            width=44,
                            height=44,
                            fit=ft.ImageFit.COVER,
                            border_radius=22
                        ),
                        width=44,
                        height=44,
                    ),
                    ft.Column([
                        ft.Text("Dr. Akash Lan Seng", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Cardiology & Internal Specialist", size=11, color=ft.Colors.WHITE70),
                    ], spacing=1)
                ], spacing=10),
                
                ft.Container(
                    content=ft.Column([
                        ft.Text("4", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ft.Text("Days", size=9, color=ft.Colors.WHITE70),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=0),
                    padding=ft.padding.symmetric(horizontal=10, vertical=4),
                    border_radius=10,
                    bgcolor=ft.Colors.WHITE24
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),

            ft.Container(height=8),

            # Bottom white pill container with Date & Time
            ft.Container(
                content=ft.Row([
                    ft.Row([
                        ft.Icon(ft.Icons.CALENDAR_TODAY_ROUNDED, size=14, color=ft.Colors.BLUE_900),
                        ft.Text("Sunday, Nov 22, 2026", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    ], spacing=6),
                    ft.Container(width=1, height=14, bgcolor=ft.Colors.GREY_300),
                    ft.Row([
                        ft.Icon(ft.Icons.ACCESS_TIME_ROUNDED, size=14, color=ft.Colors.BLUE_900),
                        ft.Text("09:00 - 10:00 AM", size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900),
                    ], spacing=6)
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
                padding=ft.padding.symmetric(horizontal=12, vertical=10),
                border_radius=12,
                bgcolor=ft.Colors.WHITE
            )
        ], spacing=4),
        padding=16,
        border_radius=20,
        gradient=ft.LinearGradient(
            begin=ft.alignment.top_left,
            end=ft.alignment.bottom_right,
            colors=["#1D4ED8", "#1E40AF"]
        ),
        shadow=ft.BoxShadow(spread_radius=1, blur_radius=12, color=ft.Colors.BLUE_200),
        margin=ft.padding.symmetric(horizontal=16, vertical=4)
    )

    # -------------------------------------------------------------
    # 5. "What do you need?" Action Categories
    # -------------------------------------------------------------
    needs_header = ft.Container(
        content=ft.Row([
            ft.Text("What do you need?", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.TextButton("See All", on_click=lambda _: navigate_to(2))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=2)
    )

    def create_need_button(title: str, icon_data, target_screen_idx: int):
        return ft.Container(
            content=ft.Column([
                ft.Container(
                    content=ft.Icon(icon_data, color=ft.Colors.BLUE_800, size=24),
                    width=52,
                    height=52,
                    border_radius=16,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.border.all(1, ft.Colors.GREY_200),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=4, color=ft.Colors.BLACK12),
                    alignment=ft.alignment.center
                ),
                ft.Text(title, size=11, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_GREY_800)
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
            ink=True,
            on_click=lambda _: navigate_to(target_screen_idx)
        )

    needs_row = ft.Container(
        content=ft.Row([
            create_need_button("Doctor", ft.Icons.LOCAL_HOSPITAL_ROUNDED, 1),
            create_need_button("Scan Lab", ft.Icons.DOCUMENT_SCANNER_ROUNDED, 2),
            create_need_button("Risk ML", ft.Icons.HEALTH_AND_SAFETY_ROUNDED, 3),
            create_need_button("Pharmacy", ft.Icons.MEDICATION_ROUNDED, 4),
            create_need_button("Chat Dr.", ft.Icons.CHAT_BUBBLE_ROUNDED, 1),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=6)
    )

    # -------------------------------------------------------------
    # 6. "Top Doctors" Section Carousel
    # -------------------------------------------------------------
    doctors_header = ft.Container(
        content=ft.Row([
            ft.Text("Top Doctors", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
            ft.TextButton("See All", on_click=lambda _: navigate_to(1))
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.padding.symmetric(horizontal=16, vertical=2)
    )

    def create_doctor_card(name: str, specialty: str, rating: str, reviews: str, img_src: str):
        return ft.Container(
            content=ft.Column([
                # Doctor Image with subtle circular halo
                ft.Container(
                    content=ft.Image(
                        src=img_src,
                        width=140,
                        height=125,
                        fit=ft.ImageFit.COVER,
                        border_radius=14
                    ),
                    width=140,
                    height=125,
                    border_radius=14,
                    alignment=ft.alignment.center
                ),
                ft.Container(height=4),
                ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_GREY_900),
                ft.Text(specialty, size=10, color=ft.Colors.GREY_600),
                ft.Row([
                    ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color=ft.Colors.AMBER_600),
                    ft.Text(f"{rating} ({reviews})", size=10, weight=ft.FontWeight.BOLD, color=ft.Colors.GREY_700),
                ], spacing=2)
            ], horizontal_alignment=ft.CrossAxisAlignment.START, spacing=2),
            width=156,
            padding=10,
            border_radius=18,
            bgcolor=ft.Colors.WHITE,
            border=ft.border.all(1, ft.Colors.GREY_200),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.BLACK12),
            ink=True,
            on_click=lambda _: navigate_to(1)
        )

    doctors_row = ft.Container(
        content=ft.Row([
            create_doctor_card("Dr. Akash Sharma", "Cardiology Specialist", "4.9", "400 Reviews", DOCTOR_MALE_IMG),
            create_doctor_card("Dr. Selena Gilndud", "Cardiology Specialist", "4.7", "320 Reviews", DOCTOR_FEMALE_IMG),
        ], spacing=12),
        padding=ft.padding.symmetric(horizontal=16, vertical=4)
    )

    # -------------------------------------------------------------
    # Screen Scrollable Assembly
    # -------------------------------------------------------------
    return ft.ListView(
        controls=[
            status_bar,
            header_section,
            search_bar,
            appointment_header,
            appointment_card,
            needs_header,
            needs_row,
            doctors_header,
            doctors_row,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
