import flet as ft
from app.state import state
from app.utils import show_snackbar, show_dialog_modal

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

    def open_add_medicine_modal(e):
        name_input = ft.TextField(label="Medicine Name", hint_text="e.g. Metformin 500mg", dense=True)
        slot_dropdown = ft.Dropdown(
            label="Daily Slot",
            value="Morning",
            options=[
                ft.dropdown.Option("Morning"),
                ft.dropdown.Option("Afternoon"),
                ft.dropdown.Option("Night"),
            ],
            dense=True
        )

        def save_medicine(ev):
            val = (name_input.value or "").strip()
            if not val:
                show_snackbar(page, "Please enter a medicine name!", bgcolor="#DC2626")
                return
            state.medicines.append({
                "name": val,
                "timing": f"{slot_dropdown.value} • Post Meal",
                "slot": slot_dropdown.value,
                "taken": False
            })
            if hasattr(page, "pop_dialog"):
                page.pop_dialog()
            show_snackbar(page, f"Added reminder for {val} ({slot_dropdown.value})", bgcolor="#16A34A")
            render_medicine_list()
            page.update()

        dialog_content = ft.Column([
            name_input,
            slot_dropdown,
            ft.FilledButton("Save Reminder", on_click=save_medicine, style=ft.ButtonStyle(bgcolor="#2563EB"))
        ], tight=True, spacing=12)
        show_dialog_modal(page, "Add Medicine Reminder", dialog_content)

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
                on_click=open_add_medicine_modal
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

    medicines_column = ft.Column(spacing=6)

    def toggle_dose(idx: int, is_checked: bool):
        state.medicines[idx]["taken"] = is_checked
        med_name = state.medicines[idx]["name"]
        msg = f"Marked {med_name} as taken!" if is_checked else f"Marked {med_name} as pending."
        show_snackbar(page, msg, bgcolor="#16A34A" if is_checked else "#334155")
        page.update()

    def render_medicine_list():
        cards = []
        for idx, med in enumerate(state.medicines):
            is_taken = med.get("taken", False)
            cb = ft.Checkbox(
                value=is_taken,
                fill_color={ft.ControlState.SELECTED: "#22C55E"},
                on_change=lambda e, i=idx: toggle_dose(i, e.control.value)
            )

            card = ft.Container(
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
                        ft.Text(med["name"], size=13, weight=ft.FontWeight.BOLD, color="#0F172A"),
                        ft.Text(f"{med['timing']}", size=11, color="#64748B"),
                    ], expand=True, spacing=1),
                    cb
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=12,
                border_radius=16,
                bgcolor=ft.Colors.WHITE,
                border=ft.Border.all(1, "#E2E8F0"),
                margin=ft.Padding.symmetric(horizontal=18, vertical=3)
            )
            cards.append(card)

        medicines_column.controls = cards

    render_medicine_list()

    return ft.ListView(
        controls=[
            status_bar,
            header,
            streak_card,
            ft.Container(
                content=ft.Text("Today's Dosage Schedule", size=15, weight=ft.FontWeight.BOLD, color="#0F172A"),
                padding=ft.Padding.symmetric(horizontal=18, vertical=6)
            ),
            medicines_column,
            ft.Container(height=35)
        ],
        spacing=4,
        padding=0
    )
