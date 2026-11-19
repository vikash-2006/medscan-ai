"""
Reusable UI components shared across all screens.
Eliminates code duplication and ensures visual consistency.
"""
import flet as ft
from app.theme import theme


def status_bar():
    """iOS-style status bar with time, signal, wifi, battery."""
    return ft.Container(
        content=ft.Row([
            ft.Text("9:41", size=13, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
            ft.Row([
                ft.Icon(ft.Icons.SIGNAL_CELLULAR_ALT_ROUNDED, size=15, color=theme.text_primary()),
                ft.Icon(ft.Icons.WIFI_ROUNDED, size=15, color=theme.text_primary()),
                ft.Icon(ft.Icons.BATTERY_FULL_ROUNDED, size=16, color=theme.text_primary()),
            ], spacing=6)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )


def back_header(title: str, navigate_to, target: str = "home", trailing: ft.Control = None):
    """Reusable header with back button, title, and optional trailing action."""
    row_children = [
        ft.Container(
            content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color=theme.text_primary(), size=18),
            width=38, height=38, border_radius=19,
            bgcolor=theme.card_bg(),
            border=ft.Border.all(1, theme.border()),
            alignment=ft.Alignment.CENTER,
            ink=True,
            on_click=lambda _: navigate_to(target)
        ),
        ft.Text(title, size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
    ]
    if trailing:
        row_children.append(trailing)
    else:
        row_children.append(ft.Container(width=38))

    return ft.Container(
        content=ft.Row(row_children, alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.symmetric(horizontal=18, vertical=6)
    )


def doctor_card(doc: dict, on_book=None, on_fav=None):
    """Reusable doctor listing card."""
    is_today = doc.get("is_today", True)
    badge_bg = theme.SUCCESS_BG if is_today else theme.WARNING_BG
    badge_color = "#16A34A" if is_today else "#D97706"

    return ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text(doc["name"], size=14, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
                    ft.Text(f"{doc['specialty']} • {doc.get('fee', '₹500')}", size=11, color=theme.text_secondary()),
                    ft.Row([
                        ft.Icon(ft.Icons.STAR_ROUNDED, size=15, color=theme.STAR),
                        ft.Text(doc.get("rating", "4.8"), size=11, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
                        ft.Text(f"({doc.get('reviews', '0')})", size=10, color=theme.text_muted()),
                    ], spacing=3),
                    ft.Container(
                        content=ft.Row([
                            ft.Container(width=6, height=6, border_radius=3, bgcolor=badge_color),
                            ft.Text(doc.get("availability", "Available"), size=10, weight=ft.FontWeight.W_600, color=badge_color)
                        ], spacing=4),
                        padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                        border_radius=6, bgcolor=badge_bg
                    )
                ], spacing=3, expand=True),
                ft.Column([
                    ft.Container(
                        content=ft.Text("Book", size=12, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        padding=ft.Padding.symmetric(horizontal=18, vertical=8),
                        border_radius=14, bgcolor=theme.PRIMARY, ink=True,
                        on_click=lambda _, item=doc: on_book(item) if on_book else None
                    )
                ], horizontal_alignment=ft.CrossAxisAlignment.END)
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER)
        ]),
        padding=14, border_radius=20,
        bgcolor=theme.card_bg(),
        border=ft.Border.all(1, theme.border()),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000")),
        margin=ft.Padding.symmetric(horizontal=18, vertical=4),
        ink=True, on_click=lambda _, item=doc: on_book(item) if on_book else None
    )


def vital_pill(label: str, val: str):
    """Compact vital statistic pill."""
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=10, color=theme.text_secondary()),
            ft.Text(val, size=13, weight=ft.FontWeight.BOLD, color=theme.text_primary())
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
        width=100,
        padding=ft.Padding.symmetric(vertical=10),
        bgcolor=theme.card_bg(),
        border_radius=14,
        border=ft.Border.all(1, theme.border())
    )


def menu_tile(icon_data, title: str, subtitle: str, on_click=None):
    """Reusable settings/menu row item."""
    return ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(icon_data, color=theme.PRIMARY, size=20),
                width=38, height=38, border_radius=12,
                bgcolor=theme.SECONDARY, alignment=ft.Alignment.CENTER
            ),
            ft.Column([
                ft.Text(title, size=13, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
                ft.Text(subtitle, size=11, color=theme.text_secondary()),
            ], expand=True, spacing=1),
            ft.Icon(ft.Icons.ARROW_FORWARD_IOS_ROUNDED, size=14, color=theme.text_muted())
        ], spacing=10),
        padding=12, border_radius=16,
        bgcolor=theme.card_bg(),
        border=ft.Border.all(1, theme.border()),
        margin=ft.Padding.symmetric(horizontal=18, vertical=3),
        ink=True, on_click=on_click
    )


def loading_shimmer(width=None, height=60):
    """Shimmer/skeleton loading placeholder."""
    return ft.Container(
        content=ft.ProgressRing(width=20, height=20, stroke_width=2),
        width=width, height=height,
        border_radius=14,
        bgcolor=theme.card_bg(),
        border=ft.Border.all(1, theme.border()),
        alignment=ft.Alignment.CENTER,
        margin=ft.Padding.symmetric(horizontal=18, vertical=4)
    )
