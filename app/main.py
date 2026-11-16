import sys
import os
import types

# ---------------------------------------------------------------------------
# Android Packaging & Module Resolution Setup
# ---------------------------------------------------------------------------
# When serious_python runs main.py inside the Android APK root directory
# (e.g. /tmp/serious_python_temp.../main.py), 'app' does not exist as a subfolder.
# We ensure the script directory is in sys.path and register an 'app' module
# alias in sys.modules so all 'from app... import ...' imports succeed.
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if "app" not in sys.modules:
    app_mod = types.ModuleType("app")
    app_mod.__path__ = [current_dir]
    app_mod.__file__ = os.path.join(current_dir, "__init__.py")
    sys.modules["app"] = app_mod

import flet as ft

# ---------------------------------------------------------------------------
# Flet 1.1+ Compatibility Shims
# ---------------------------------------------------------------------------
# 1. Colors enum aliases (BLACK87 -> BLACK_87, WHITE70 -> WHITE_70, etc.)
if hasattr(ft, "Colors"):
    for _name in list(dir(ft.Colors)):
        if "_" in _name:
            _alias = _name.replace("_", "")
            try:
                setattr(ft.Colors, _alias, getattr(ft.Colors, _name))
            except Exception:
                pass
    ft.colors = ft.Colors

# 2. Controls & Properties
if hasattr(ft, "Padding"):
    ft.padding = ft.Padding
if hasattr(ft, "BorderRadius"):
    ft.border_radius = ft.BorderRadius
if hasattr(ft, "Margin"):
    ft.margin = ft.Margin
if hasattr(ft, "Border"):
    ft.border = ft.Border
if hasattr(ft, "BoxFit"):
    ft.ImageFit = ft.BoxFit
if hasattr(ft, "Button") and not hasattr(ft, "ElevatedButton"):
    ft.ElevatedButton = ft.Button

# 3. Chip avatar -> leading compatibility wrapper
if hasattr(ft, "Chip") and not hasattr(ft, "ActionChip"):
    def _ActionChip(**kwargs):
        if "avatar" in kwargs:
            kwargs["leading"] = kwargs.pop("avatar")
        return ft.Chip(**kwargs)
    ft.ActionChip = _ActionChip

# 4. Alignment lowercase properties
if hasattr(ft, "Alignment"):
    for _name in [
        "CENTER", "TOP_LEFT", "TOP_RIGHT", "BOTTOM_LEFT", "BOTTOM_RIGHT",
        "TOP_CENTER", "BOTTOM_CENTER", "CENTER_LEFT", "CENTER_RIGHT"
    ]:
        if hasattr(ft.Alignment, _name):
            try:
                setattr(ft.Alignment, _name.lower(), getattr(ft.Alignment, _name))
            except Exception:
                pass
    ft.alignment = ft.Alignment

# 5. App runner
if not hasattr(ft, "app") and hasattr(ft, "run"):
    ft.app = ft.run

# ---------------------------------------------------------------------------
# Application Imports
# ---------------------------------------------------------------------------
from app.state import state
from app.screens.android_home_screen import build_android_home_screen
from app.screens.android_consult_screen import build_android_consult_screen
from app.screens.scan_screen import build_scan_screen
from app.screens.risk_screen import build_risk_screen
from app.screens.history_screen import build_history_screen

def main(page: ft.Page):
    page.title = "MedScan AI — Android Mobile App"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.bgcolor = "#F8FAFC"
    page.padding = 0

    # Mobile frame simulator default sizing for desktop test
    try:
        if hasattr(page, "window") and page.window:
            page.window.width = 412
            page.window.height = 880
            page.window.resizable = True
    except Exception:
        pass

    current_index = 0
    main_content_area = ft.Container(expand=True, bgcolor="#F8FAFC")
    nav_container = ft.Container()

    def build_bottom_nav(selected_idx: int):
        def create_nav_item(idx: int, icon_data, label: str):
            is_active = (idx == selected_idx)
            if is_active:
                return ft.Container(
                    content=ft.Row([
                        ft.Icon(icon_data, color=ft.Colors.WHITE, size=18),
                        ft.Text(label, size=11, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE)
                    ], spacing=5),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=8),
                    border_radius=18,
                    bgcolor="#2563EB",  # Vibrant Royal Blue active pill
                    ink=True,
                    on_click=lambda _: navigate_to(idx)
                )
            else:
                return ft.Container(
                    content=ft.Icon(icon_data, color=ft.Colors.WHITE_70, size=22),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=8),
                    ink=True,
                    on_click=lambda _: navigate_to(idx)
                )

        return ft.Container(
            content=ft.Row([
                create_nav_item(0, ft.Icons.HOME_ROUNDED, "Home"),
                create_nav_item(1, ft.Icons.CALENDAR_MONTH_ROUNDED, "Visits"),
                create_nav_item(2, ft.Icons.DOCUMENT_SCANNER_ROUNDED, "Scan Lab"),
                create_nav_item(3, ft.Icons.HEALTH_AND_SAFETY_ROUNDED, "Risk ML"),
                create_nav_item(4, ft.Icons.HISTORY_ROUNDED, "History"),
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            border_radius=28,
            bgcolor="#1E3A8A",  # Deep Blue matching the reference UI
            shadow=ft.BoxShadow(spread_radius=1, blur_radius=14, color=ft.Colors.BLACK_26),
            margin=ft.Padding.symmetric(horizontal=16, vertical=8)
        )

    def navigate_to(index: int):
        nonlocal current_index
        current_index = index

        if index == 0:
            main_content_area.content = build_android_home_screen(page, navigate_to)
        elif index == 1:
            main_content_area.content = build_android_consult_screen(page, navigate_to)
        elif index == 2:
            main_content_area.content = build_scan_screen(page, navigate_to)
        elif index == 3:
            main_content_area.content = build_risk_screen(page, navigate_to)
        elif index == 4:
            main_content_area.content = build_history_screen(page, navigate_to)

        nav_container.content = build_bottom_nav(current_index)
        page.update()

    # Initial setup
    nav_container.content = build_bottom_nav(0)
    navigate_to(0)

    # Page layout: Main content scroll on top + fixed floating deep blue navbar at bottom
    page.add(
        ft.Column([
            main_content_area,
            nav_container
        ], expand=True, spacing=0)
    )

if __name__ == "__main__":
    assets_path = os.path.join(current_dir, "assets")
    if hasattr(ft, "run"):
        ft.run(main, assets_dir=assets_path if os.path.exists(assets_path) else "assets")
    elif hasattr(ft, "app"):
        ft.app(main, assets_dir=assets_path if os.path.exists(assets_path) else "assets")
