import os
import flet as ft
from app.state import state
from app.utils import show_snackbar

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

def build_sanjeevani_profile_screen(page: ft.Page, navigate_to) -> ft.Control:
    # Get active doctor data from state
    doc = state.selected_doctor or {
        "name": "Dr. Rohan Mehta",
        "specialty": "General Physician",
        "rating": "4.8",
        "reviews": "1,240",
        "experience": "7+ Years",
        "patients": "2.5K+",
        "avatar": "doctor_portrait.jpg",
        "fee": "₹500",
        "about": "Senior Consultant Physician specializing in internal medicine, lifestyle disorders, and preventive health management."
    }

    doc_avatar = _get_asset(doc.get("avatar", "doctor_portrait.jpg"))

    # State variables for interactivity
    active_tab = "Book"
    selected_date_str = "Tue, 17 Nov"
    selected_time_str = "11:00 AM"

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
    is_favorite = False
    favorite_icon = ft.Icon(ft.Icons.FAVORITE_BORDER_ROUNDED, color="#0F172A", size=18)

    def toggle_favorite(e):
        nonlocal is_favorite
        is_favorite = not is_favorite
        favorite_icon.name = ft.Icons.FAVORITE_ROUNDED if is_favorite else ft.Icons.FAVORITE_BORDER_ROUNDED
        favorite_icon.color = "#EF4444" if is_favorite else "#0F172A"
        msg = f"Added {doc['name']} to Favorites!" if is_favorite else f"Removed {doc['name']} from Favorites."
        show_snackbar(page, msg, bgcolor="#EF4444" if is_favorite else "#334155")
        page.update()

    def handle_share(e):
        show_snackbar(page, f"Consultation profile link copied for {doc['name']}!", bgcolor="#2563EB")

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
                    content=favorite_icon,
                    width=38,
                    height=38,
                    border_radius=19,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, "#E2E8F0"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                    on_click=toggle_favorite
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
                    on_click=handle_share
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
                    src=doc_avatar,
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
                ft.Text(doc["name"], size=20, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Icon(ft.Icons.VERIFIED_ROUNDED, size=18, color="#2563EB")
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=4),
            ft.Text(f"{doc['specialty']} • Consultation Fee: {doc.get('fee', '₹500')}", size=12, color="#64748B"),
            ft.Row([
                ft.Icon(ft.Icons.STAR_ROUNDED, size=16, color="#F59E0B"),
                ft.Text(doc["rating"], size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text(f"({doc['reviews']} Reviews)", size=12, color="#94A3B8"),
            ], alignment=ft.MainAxisAlignment.CENTER, spacing=3)
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
        padding=ft.Padding.symmetric(vertical=8),
        alignment=ft.Alignment.CENTER
    )

    # 4. Three Stat Badges
    stats_row = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.HISTORY_TOGGLE_OFF_ROUNDED, color="#2563EB", size=22),
                    ft.Text(doc.get("experience", "7+ Years"), size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("Experience", size=10, color="#64748B")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                width=100,
                padding=ft.Padding.symmetric(vertical=10, horizontal=6),
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                border=ft.Border.all(1, "#E2E8F0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000"))
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.PEOPLE_ALT_ROUNDED, color="#2563EB", size=22),
                    ft.Text(doc.get("patients", "2.5K+"), size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("Patients", size=10, color="#64748B")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                width=100,
                padding=ft.Padding.symmetric(vertical=10, horizontal=6),
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                border=ft.Border.all(1, "#E2E8F0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000"))
            ),
            ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.STAR_ROUNDED, color="#2563EB", size=22),
                    ft.Text("98%", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text("Rating", size=10, color="#64748B")
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                width=100,
                padding=ft.Padding.symmetric(vertical=10, horizontal=6),
                bgcolor=ft.Colors.WHITE,
                border_radius=16,
                border=ft.Border.all(1, "#E2E8F0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=6, color=ft.Colors.with_opacity(0.04, "#000000"))
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=4)
    )

    # 5. Interactive Tab Content Container
    tab_content_area = ft.Container()

    # Dates definition
    dates_list = [
        ("Tue", "17 Nov", "Tue, 17 Nov"),
        ("Wed", "18 Nov", "Wed, 18 Nov"),
        ("Thu", "19 Nov", "Thu, 19 Nov"),
        ("Fri", "20 Nov", "Fri, 20 Nov"),
    ]

    # Times definition
    times_list = ["10:00 AM", "11:00 AM", "02:00 PM", "04:30 PM"]

    def select_date(full_date: str):
        nonlocal selected_date_str
        selected_date_str = full_date
        render_tab_view()
        page.update()

    def select_time(time_val: str):
        nonlocal selected_time_str
        selected_time_str = time_val
        render_tab_view()
        page.update()

    def build_booking_panel():
        date_pills = []
        for day, dt, full_dt in dates_list:
            is_active = (selected_date_str == full_dt)
            date_pills.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text(day, size=11, weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.NORMAL,
                                color=ft.Colors.WHITE if is_active else "#64748B"),
                        ft.Text(dt, size=13, weight=ft.FontWeight.BOLD,
                                color=ft.Colors.WHITE if is_active else "#0F172A"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    border_radius=16,
                    bgcolor="#2563EB" if is_active else ft.Colors.WHITE,
                    border=None if is_active else ft.Border.all(1, "#E2E8F0"),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.3, "#2563EB")) if is_active else None,
                    ink=True,
                    on_click=lambda _, f=full_dt: select_date(f)
                )
            )

        time_pills = []
        for tm in times_list:
            is_active = (selected_time_str == tm)
            time_pills.append(
                ft.Container(
                    content=ft.Text(tm, size=12, weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500,
                                    color=ft.Colors.WHITE if is_active else "#0F172A"),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                    border_radius=14,
                    bgcolor="#2563EB" if is_active else ft.Colors.WHITE,
                    border=None if is_active else ft.Border.all(1, "#E2E8F0"),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.3, "#2563EB")) if is_active else None,
                    ink=True,
                    on_click=lambda _, t=tm: select_time(t)
                )
            )

        return ft.Column([
            ft.Container(
                content=ft.Column([
                    ft.Text("Select Date", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Row(date_pills, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                ], spacing=8),
                padding=ft.Padding.symmetric(horizontal=18, vertical=6)
            ),
            ft.Container(
                content=ft.Column([
                    ft.Text("Select Time", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Row(time_pills, spacing=8)
                ], spacing=8),
                padding=ft.Padding.symmetric(horizontal=18, vertical=6)
            )
        ], spacing=4)

    def build_about_panel():
        return ft.Container(
            content=ft.Column([
                ft.Text("About Doctor", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text(doc.get("about", "Specialist physician dedicated to evidence-based healthcare."),
                        size=12, color="#475569", line_height=1.4),
                ft.Container(height=6),
                ft.Text("Certifications & Hospital Affiliations", size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("• MBBS, MD (Internal Medicine), AIIMS New Delhi\n• Member of Indian Medical Association (IMA)\n• Sanjeevani Tele-Consultation Advisory Board",
                        size=11, color="#64748B", line_height=1.4),
            ], spacing=6),
            padding=ft.Padding.symmetric(horizontal=18, vertical=8)
        )

    def build_reviews_panel():
        return ft.Container(
            content=ft.Column([
                ft.Text("Patient Reviews (1,240)", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Pooja Sharma", size=12, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Row([
                                ft.Icon(ft.Icons.STAR_ROUNDED, size=14, color="#F59E0B"),
                                ft.Text("5.0", size=11, weight=ft.FontWeight.BOLD)
                            ], spacing=2)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text("Doctor Mehta explained my blood sugar report with great patience and gave practical diet tips. Highly recommended!",
                                size=11, color="#64748B"),
                    ], spacing=2),
                    padding=10,
                    border_radius=12,
                    bgcolor=ft.Colors.WHITE,
                    border=ft.Border.all(1, "#E2E8F0")
                ),
            ], spacing=8),
            padding=ft.Padding.symmetric(horizontal=18, vertical=8)
        )

    def render_tab_view():
        if active_tab == "Book":
            tab_content_area.content = build_booking_panel()
            bottom_action_bar.visible = True
        elif active_tab == "About":
            tab_content_area.content = build_about_panel()
            bottom_action_bar.visible = True
        else:
            tab_content_area.content = build_reviews_panel()
            bottom_action_bar.visible = True

    def switch_tab(tab_name: str):
        nonlocal active_tab
        active_tab = tab_name
        # Re-render segmented tabs visual state
        book_tab.bgcolor = "#2563EB" if tab_name == "Book" else None
        book_tab.content.color = ft.Colors.WHITE if tab_name == "Book" else "#64748B"
        book_tab.content.weight = ft.FontWeight.BOLD if tab_name == "Book" else ft.FontWeight.W_500

        about_tab.bgcolor = "#2563EB" if tab_name == "About" else None
        about_tab.content.color = ft.Colors.WHITE if tab_name == "About" else "#64748B"
        about_tab.content.weight = ft.FontWeight.BOLD if tab_name == "About" else ft.FontWeight.W_500

        reviews_tab.bgcolor = "#2563EB" if tab_name == "Reviews" else None
        reviews_tab.content.color = ft.Colors.WHITE if tab_name == "Reviews" else "#64748B"
        reviews_tab.content.weight = ft.FontWeight.BOLD if tab_name == "Reviews" else ft.FontWeight.W_500

        render_tab_view()
        page.update()

    book_tab = ft.Container(
        content=ft.Text("Book", size=13, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
        padding=ft.Padding.symmetric(horizontal=20, vertical=8),
        border_radius=14,
        bgcolor="#2563EB",
        expand=True,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=lambda _: switch_tab("Book")
    )
    about_tab = ft.Container(
        content=ft.Text("About", size=13, weight=ft.FontWeight.W_500, color="#64748B"),
        padding=ft.Padding.symmetric(horizontal=20, vertical=8),
        border_radius=14,
        expand=True,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=lambda _: switch_tab("About")
    )
    reviews_tab = ft.Container(
        content=ft.Text("Reviews", size=13, weight=ft.FontWeight.W_500, color="#64748B"),
        padding=ft.Padding.symmetric(horizontal=20, vertical=8),
        border_radius=14,
        expand=True,
        alignment=ft.Alignment.CENTER,
        ink=True,
        on_click=lambda _: switch_tab("Reviews")
    )

    segmented_tabs = ft.Container(
        content=ft.Row([book_tab, about_tab, reviews_tab]),
        padding=4,
        border_radius=18,
        bgcolor="#F1F5F9",
        margin=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 6. Bottom CTA Button: "Confirm Booking"
    def handle_confirm_booking(e):
        # Save appointment in application state
        new_appointment = {
            "doctor_name": doc["name"],
            "specialty": f"{doc['specialty']} • Consultation",
            "date_str": selected_date_str + " 2026",
            "time_str": selected_time_str,
            "status": "Confirmed",
            "avatar": doc.get("avatar", "doctor_portrait.jpg"),
            "fee": doc.get("fee", "₹500")
        }
        # Prepend to active appointments
        state.booked_appointments.insert(0, new_appointment)

        show_snackbar(
            page,
            f"Appointment Confirmed with {doc['name']} for {selected_date_str} at {selected_time_str}!",
            bgcolor="#16A34A"
        )
        navigate_to("appointments")

    confirm_btn = ft.Container(
        content=ft.Row([
            ft.Icon(ft.Icons.CALENDAR_MONTH_ROUNDED, color=ft.Colors.WHITE, size=18),
            ft.Text(f"Confirm Booking ({doc.get('fee', '₹500')})", size=15, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
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

    # Initial render
    render_tab_view()

    # Assembly
    return ft.Column([
        ft.Container(
            content=ft.ListView(
                controls=[
                    status_bar,
                    header,
                    doctor_info_card,
                    stats_row,
                    segmented_tabs,
                    tab_content_area,
                    ft.Container(height=20)
                ],
                spacing=4,
                padding=0
            ),
            expand=True
        ),
        bottom_action_bar
    ], expand=True, spacing=0)
