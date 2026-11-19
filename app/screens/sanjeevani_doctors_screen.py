import os
import flet as ft
from app.state import state
from app.utils import show_snackbar

_BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_ASSETS_DIR = os.path.join(_BASE_DIR, "assets")

def _get_asset(filename: str) -> str:
    path = os.path.join(_ASSETS_DIR, filename)
    return path if os.path.exists(path) else f"/{filename}"

DOCTORS_DATABASE = [
    {
        "id": "dr_rohan",
        "name": "Dr. Rohan Mehta",
        "specialty": "General Physician",
        "category": "General",
        "rating": "4.8",
        "reviews": "1,240",
        "availability": "Available Today",
        "is_today": True,
        "avatar": "doctor_portrait.jpg",
        "experience": "7+ Years",
        "patients": "2.5K+",
        "fee": "₹500",
        "about": "Dr. Rohan Mehta is a Senior Consultant Physician specializing in primary care, chronic condition management (Diabetes, Hypertension), and preventive health screenings."
    },
    {
        "id": "dr_ananya",
        "name": "Dr. Ananya Sharma",
        "specialty": "Cardiologist",
        "category": "Cardiology",
        "rating": "4.9",
        "reviews": "980",
        "availability": "Available Today",
        "is_today": True,
        "avatar": "doctor_female.jpg",
        "experience": "9+ Years",
        "patients": "3.1K+",
        "fee": "₹700",
        "about": "Dr. Ananya Sharma is an experienced Interventional Cardiologist specializing in preventive cardiac care, ECG/Echo review, and lipid metabolic optimization."
    },
    {
        "id": "dr_vivek",
        "name": "Dr. Vivek Singh",
        "specialty": "Gastroenterologist",
        "category": "General",
        "rating": "4.7",
        "reviews": "750",
        "availability": "Available Tomorrow",
        "is_today": False,
        "avatar": "doctor_male_2.jpg",
        "experience": "6+ Years",
        "patients": "1.8K+",
        "fee": "₹600",
        "about": "Dr. Vivek Singh is a leading specialist in digestive disorders, liver health, and post-operative dietary recovery with extensive clinical experience."
    },
    {
        "id": "dr_priya",
        "name": "Dr. Priya Patel",
        "specialty": "Dermatologist & Cosmetologist",
        "category": "Dermatology",
        "rating": "4.9",
        "reviews": "1,120",
        "availability": "Available Today",
        "is_today": True,
        "avatar": "doctor_female.jpg",
        "experience": "8+ Years",
        "patients": "2.9K+",
        "fee": "₹650",
        "about": "Dr. Priya Patel provides specialized dermatological care for skin allergies, hormonal acne, anti-aging therapies, and hair restoration."
    }
]

def build_sanjeevani_doctors_screen(page: ft.Page, navigate_to) -> ft.Control:
    selected_filter = "All"
    search_query = ""

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

    # Search Bar Toggle State
    search_visible = False
    search_container = ft.Container(visible=False)

    def toggle_search_box(e):
        nonlocal search_visible
        search_visible = not search_visible
        search_container.visible = search_visible
        page.update()

    # 2. Header
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
            ft.Text("Find Doctors", size=18, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(
                content=ft.Icon(ft.Icons.SEARCH_ROUNDED, color="#0F172A", size=20),
                width=38,
                height=38,
                border_radius=19,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=toggle_search_box
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    def on_search_change(e):
        nonlocal search_query
        search_query = (e.control.value or "").lower().strip()
        render_doctors_list()
        page.update()

    search_field = ft.TextField(
        hint_text="Search doctor name or specialization...",
        dense=True,
        border=ft.InputBorder.OUTLINE,
        border_radius=14,
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        text_size=13,
        on_change=on_search_change
    )
    search_container.content = ft.Container(content=search_field, padding=ft.Padding.symmetric(horizontal=18, vertical=4))

    # 3. Filter Chips
    categories = ["All", "General", "Cardiology", "Dermatology"]
    filter_chips_row = ft.Row(spacing=8, scroll=ft.ScrollMode.HIDDEN)

    def set_filter(cat: str):
        nonlocal selected_filter
        selected_filter = cat
        render_filter_chips()
        render_doctors_list()
        page.update()

    def render_filter_chips():
        chips = []
        for cat in categories:
            is_active = (selected_filter == cat)
            chips.append(
                ft.Container(
                    content=ft.Text(
                        cat,
                        size=12,
                        weight=ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500,
                        color=ft.Colors.WHITE if is_active else "#64748B"
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=8),
                    border_radius=20,
                    bgcolor="#2563EB" if is_active else ft.Colors.WHITE,
                    border=None if is_active else ft.Border.all(1, "#E2E8F0"),
                    shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.25, "#2563EB")) if is_active else None,
                    ink=True,
                    on_click=lambda _, c=cat: set_filter(c)
                )
            )
        filter_chips_row.controls = chips

    filter_section = ft.Container(
        content=filter_chips_row,
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # 4. Doctor List Container
    doctors_column = ft.Column(spacing=8)

    def book_doctor(doc: dict):
        state.selected_doctor = doc
        navigate_to("profile")

    def toggle_fav(e, doc_name: str):
        show_snackbar(page, f"Updated favorite preference for {doc_name}", bgcolor="#2563EB")

    def render_doctors_list():
        cards = []
        filtered = [
            d for d in DOCTORS_DATABASE
            if (selected_filter == "All" or d["category"] == selected_filter) and
               (not search_query or search_query in d["name"].lower() or search_query in d["specialty"].lower())
        ]

        if not filtered:
            cards.append(
                ft.Container(
                    content=ft.Column([
                        ft.Icon(ft.Icons.PERSON_SEARCH_ROUNDED, size=48, color="#94A3B8"),
                        ft.Text("No doctors found for this filter.", size=13, color="#64748B"),
                    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=6),
                    padding=32,
                    alignment=ft.Alignment.CENTER
                )
            )

        for d in filtered:
            is_today = d["is_today"]
            badge_bg = "#DCFCE7" if is_today else "#FEF3C7"
            badge_color = "#16A34A" if is_today else "#D97706"
            avatar_path = _get_asset(d["avatar"])

            card = ft.Container(
                content=ft.Column([
                    ft.Row([
                        # Doctor Image
                        ft.Image(
                            src=avatar_path,
                            width=64,
                            height=64,
                            fit=ft.BoxFit.COVER,
                            border_radius=16
                        ),
                        # Doctor Details
                        ft.Column([
                            ft.Text(d["name"], size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                            ft.Text(f"{d['specialty']} • {d.get('fee', '₹500')}", size=11, color="#64748B"),
                            ft.Row([
                                ft.Icon(ft.Icons.STAR_ROUNDED, size=15, color="#F59E0B"),
                                ft.Text(d["rating"], size=11, weight=ft.FontWeight.BOLD, color="#0F172A"),
                                ft.Text(f"({d['reviews']})", size=10, color="#94A3B8"),
                            ], spacing=3),
                            ft.Container(
                                content=ft.Row([
                                    ft.Container(width=6, height=6, border_radius=3, bgcolor=badge_color),
                                    ft.Text(d["availability"], size=10, weight=ft.FontWeight.W_600, color=badge_color)
                                ], spacing=4),
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                                border_radius=6,
                                bgcolor=badge_bg
                            )
                        ], spacing=3, expand=True),

                        # Favorite & Book Button
                        ft.Column([
                            ft.IconButton(
                                icon=ft.Icons.FAVORITE_BORDER_ROUNDED,
                                icon_color="#94A3B8",
                                icon_size=18,
                                on_click=lambda _, name=d["name"]: toggle_fav(_, name)
                            ),
                            ft.Container(
                                content=ft.Text("Book", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                                padding=ft.Padding.symmetric(horizontal=18, vertical=8),
                                border_radius=14,
                                bgcolor="#2563EB",
                                ink=True,
                                on_click=lambda _, item=d: book_doctor(item)
                            )
                        ], horizontal_alignment=ft.CrossAxisAlignment.END)
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
                ]),
                padding=14,
                border_radius=20,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000")),
                margin=ft.Padding.symmetric(horizontal=18, vertical=4),
                ink=True,
                on_click=lambda _, item=d: book_doctor(item)
            )
            cards.append(card)

        doctors_column.controls = cards

    # Initial renders
    render_filter_chips()
    render_doctors_list()

    return ft.ListView(
        controls=[
            status_bar,
            header,
            search_container,
            filter_section,
            doctors_column,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
