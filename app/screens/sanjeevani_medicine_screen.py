import flet as ft

def build_sanjeevani_medicine_screen(page: ft.Page, navigate_to) -> ft.Control:
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
            ft.Text("Medicine Reminder", size=18, weight=ft.FontWeight.BOLD, color="#0F172A"),
            ft.Container(
                content=ft.Icon(ft.Icons.ADD_ROUNDED, color="#2563EB", size=22),
                width=38,
                height=38,
                border_radius=19,
                bgcolor="#EAF4FF",
                alignment=ft.Alignment.CENTER,
                ink=True,
                on_click=lambda _: page.open(ft.SnackBar(ft.Text("Add new medicine reminder dialog")))
            ),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )

    # Streak Card
    streak_card = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.LOCAL_FIRE_DEPARTMENT_ROUNDED, color="#F59E0B", size=28),
                width=48,
                height=48,
                border_radius=16,
                bgcolor="#FEF3C7",
                alignment=ft.Alignment.CENTER
            ),
            ft.Column([
                ft.Text("5-Day Medication Streak! 🔥", size=14, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text("All prescribed doses taken on schedule this week.", size=11, color="#64748B"),
            ], expand=True, spacing=1)
        ], spacing=10),
        padding=14,
        border_radius=18,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, "#E2E8F0"),
        margin=ft.Padding.symmetric(horizontal=18, vertical=6),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000"))
    )

    def create_dose_item(name: str, timing: str, dosage: str, is_taken: bool):
        cb = ft.Checkbox(value=is_taken, fill_color={ft.ControlState.SELECTED: "#22C55E"})
        return ft.Container(
            content=ft.Row([
                ft.Container(
                    content=ft.Icon(ft.Icons.MEDICATION_ROUNDED, color="#2563EB", size=22),
                    width=42,
                    height=42,
                    border_radius=14,
                    bgcolor="#EAF4FF",
                    alignment=ft.Alignment.CENTER
                ),
                ft.Column([
                    ft.Text(name, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                    ft.Text(f"{dosage} • {timing}", size=11, color="#64748B"),
                ], expand=True, spacing=1),
                cb
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=12,
            border_radius=16,
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.all(1, "#E2E8F0"),
            margin=ft.Padding.symmetric(horizontal=18, vertical=4)
        )

    def create_time_header(title: str, time_str: str):
        return ft.Container(
            content=ft.Row([
                ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                ft.Text(time_str, size=11, weight=ft.FontWeight.W_600, color="#2563EB"),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.Padding.symmetric(horizontal=18, vertical=6)
        )

    return ft.ListView(
        controls=[
            status_bar,
            header,
            streak_card,
            create_time_header("Morning Dose", "08:00 AM"),
            create_dose_item("Metformin HCl", "After Breakfast", "500 mg • 1 Tablet", True),
            create_dose_item("Atorvastatin", "After Breakfast", "10 mg • 1 Tablet", True),
            create_time_header("Afternoon Dose", "01:30 PM"),
            create_dose_item("Vitamin D3 Calcirol", "After Lunch", "60,000 IU • Weekly", False),
            create_time_header("Night Dose", "09:00 PM"),
            create_dose_item("Telmisartan BP Care", "Before Bed", "40 mg • 1 Tablet", False),
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
