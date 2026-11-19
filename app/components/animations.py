"""
Micro-animation utilities for MedScan AI.
Provides scale-on-tap and fade-in effects for premium feel.
"""
import flet as ft
from app.theme import theme


def animated_button(text: str, on_click=None, icon=None, bgcolor=None, color=None, width=None):
    """Button with scale animation on tap — premium feel."""
    bg = bgcolor or theme.PRIMARY
    fg = color or "#FFFFFF"

    btn_content = ft.Row(
        [
            *([] if not icon else [ft.Icon(icon, color=fg, size=18)]),
            ft.Text(text, weight=ft.FontWeight.BOLD, color=fg, size=13),
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=8
    )

    return ft.Container(
        content=btn_content,
        padding=ft.Padding(20, 12, 20, 12),
        border_radius=14,
        bgcolor=bg,
        width=width,
        ink=True,
        on_click=on_click,
        animate_scale=ft.Animation(150, ft.AnimationCurve.EASE_OUT),
        scale=ft.Scale(1.0),
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=10,
            color=ft.Colors.with_opacity(0.15, bg)
        )
    )


def fade_in_container(content: ft.Control, delay_ms: int = 0):
    """Wraps content with a fade-in animation."""
    return ft.AnimatedSwitcher(
        content=content,
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=400,
        switch_in_curve=ft.AnimationCurve.EASE_IN,
    )


def animated_card(content: ft.Control, on_click=None):
    """Card with subtle scale animation on tap."""
    return ft.Container(
        content=content,
        border_radius=18,
        bgcolor=theme.card_bg(),
        border=ft.Border.all(1, theme.border()),
        padding=14,
        margin=ft.Padding(18, 4, 18, 4),
        shadow=ft.BoxShadow(spread_radius=0, blur_radius=8, color=ft.Colors.with_opacity(0.04, "#000000")),
        ink=True,
        on_click=on_click,
        animate_scale=ft.Animation(120, ft.AnimationCurve.EASE_OUT),
        scale=ft.Scale(1.0),
    )
