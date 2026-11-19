import sys
import os
import types

# ---------------------------------------------------------------------------
# Android Packaging & Module Resolution Setup
# ---------------------------------------------------------------------------
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
# Flet 1.1+ Compatibility Shims & Module Monkeypatching
# ---------------------------------------------------------------------------
if hasattr(ft, "Colors"):
    for _name in list(dir(ft.Colors)):
        if "_" in _name:
            _alias = _name.replace("_", "")
            try:
                setattr(ft.Colors, _alias, getattr(ft.Colors, _name))
            except Exception:
                pass
    ft.colors = ft.Colors

if hasattr(ft, "Padding"):
    ft.padding = ft.Padding
    try:
        import flet.controls.padding as _mod_padding
        _mod_padding.symmetric = ft.Padding.symmetric
        _mod_padding.all = ft.Padding.all
        _mod_padding.only = ft.Padding.only
        _mod_padding.zero = ft.Padding.zero
    except Exception:
        pass

if hasattr(ft, "BorderRadius"):
    ft.border_radius = ft.BorderRadius
    try:
        import flet.controls.border_radius as _mod_br
        _mod_br.all = ft.BorderRadius.all
        _mod_br.only = ft.BorderRadius.only
        _mod_br.horizontal = ft.BorderRadius.horizontal
        _mod_br.vertical = ft.BorderRadius.vertical
    except Exception:
        pass

if hasattr(ft, "Margin"):
    ft.margin = ft.Margin
if hasattr(ft, "Border"):
    ft.border = ft.Border
    try:
        import flet.controls.border as _mod_border
        _mod_border.all = ft.Border.all
        _mod_border.only = ft.Border.only
        _mod_border.symmetric = ft.Border.symmetric
    except Exception:
        pass

if hasattr(ft, "BoxFit"):
    ft.ImageFit = ft.BoxFit
if hasattr(ft, "Button") and not hasattr(ft, "ElevatedButton"):
    ft.ElevatedButton = ft.Button

# Text parameter compatibility shim (e.g. line_height -> style)
if hasattr(ft, "Text"):
    _orig_text_init = ft.Text.__init__
    def _safe_text_init(self, *args, **kwargs):
        if "line_height" in kwargs:
            lh = kwargs.pop("line_height")
            if "style" not in kwargs or kwargs["style"] is None:
                kwargs["style"] = ft.TextStyle(height=lh)
        _orig_text_init(self, *args, **kwargs)
    ft.Text.__init__ = _safe_text_init

if hasattr(ft, "Chip") and not hasattr(ft, "ActionChip"):
    def _ActionChip(**kwargs):
        if "avatar" in kwargs:
            kwargs["leading"] = kwargs.pop("avatar")
        return ft.Chip(**kwargs)
    ft.ActionChip = _ActionChip

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

if not hasattr(ft, "app") and hasattr(ft, "run"):
    ft.app = ft.run

# Page.open & Page.close cross-version shims
try:
    import flet.controls.page as _fp

    def _page_open_shim(self, control):
        if hasattr(self, "show_dialog") and callable(self.show_dialog):
            try:
                return self.show_dialog(control)
            except Exception:
                pass
        if hasattr(self, "overlay"):
            if control not in self.overlay:
                self.overlay.append(control)
            if hasattr(control, "open"):
                control.open = True
            self.update()
            return control
        if hasattr(control, "open"):
            control.open = True
            self.update()
            return control

    def _page_close_shim(self, control=None):
        if hasattr(self, "pop_dialog") and callable(self.pop_dialog):
            try:
                return self.pop_dialog()
            except Exception:
                pass
        if control is not None and hasattr(control, "open"):
            control.open = False
            self.update()

    if not hasattr(_fp.Page, "open"):
        _fp.Page.open = _page_open_shim
    if not hasattr(_fp.Page, "close"):
        _fp.Page.close = _page_close_shim
    if hasattr(ft, "Page"):
        if not hasattr(ft.Page, "open"):
            ft.Page.open = _page_open_shim
        if not hasattr(ft.Page, "close"):
            ft.Page.close = _page_close_shim
except Exception:
    pass

# ---------------------------------------------------------------------------
# Screen Imports
# ---------------------------------------------------------------------------
from app.state import state
from app.screens.sanjeevani_splash_screen import build_sanjeevani_splash_screen
from app.screens.sanjeevani_home_screen import build_sanjeevani_home_screen
from app.screens.sanjeevani_doctors_screen import build_sanjeevani_doctors_screen
from app.screens.sanjeevani_profile_screen import build_sanjeevani_profile_screen
from app.screens.sanjeevani_appointments_screen import build_sanjeevani_appointments_screen
from app.screens.sanjeevani_video_screen import build_sanjeevani_video_screen
from app.screens.sanjeevani_medicine_screen import build_sanjeevani_medicine_screen
from app.screens.sanjeevani_user_profile_screen import build_sanjeevani_user_profile_screen
from app.screens.scan_screen import build_scan_screen
from app.screens.risk_screen import build_risk_screen
from app.screens.report_screen import build_report_screen

def main(page: ft.Page):
    page.title = "Sanjeevani Healthcare — Android Mobile App"
    # Theme mode & Animation support
    page.theme_mode = ft.ThemeMode.LIGHT
    
    # Mobile frame sizing for desktop simulation
    try:
        if hasattr(page, "window") and page.window:
            page.window.width = 412
            page.window.height = 880
            page.window.resizable = True
    except Exception:
        pass

    current_screen = "home"
    current_tab_index = 0
    main_content_area = ft.Container(expand=True, bgcolor="#F8FAFC")
    nav_container = ft.Container()

    # Animated switcher for smooth transitions
    animated_switcher = ft.AnimatedSwitcher(
        content=ft.Container(),
        transition=ft.AnimatedSwitcherTransition.FADE,
        duration=300,
        reverse_duration=100,
        switch_in_curve=ft.AnimationCurve.EASE_IN_OUT,
        switch_out_curve=ft.AnimationCurve.EASE_IN_OUT,
    )
    main_content_area.content = animated_switcher

    # iOS-Inspired Clean White Bottom Navigation Bar
    def build_ios_bottom_nav(active_tab: int):
        tabs = [
            (0, ft.Icons.HOME_ROUNDED, "Home", "home"),
            (1, ft.Icons.CALENDAR_MONTH_ROUNDED, "Appointments", "appointments"),
            (2, ft.Icons.FOLDER_SHARED_ROUNDED, "Records", "scan_lab"),
            (3, ft.Icons.PERSON_ROUNDED, "Profile", "user_profile"),
        ]

        def create_tab_item(idx: int, icon_data, label: str, target_route: str):
            is_active = (idx == active_tab)
            color = "#2563EB" if is_active else "#94A3B8"
            weight = ft.FontWeight.BOLD if is_active else ft.FontWeight.W_500

            return ft.Container(
                content=ft.Column([
                    ft.Icon(icon_data, color=color, size=24),
                    ft.Text(label, size=10, weight=weight, color=color)
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=2),
                padding=ft.Padding.symmetric(vertical=6, horizontal=16),
                ink=True,
                on_click=lambda _: navigate_to(target_route)
            )

        return ft.Container(
            content=ft.Row([
                create_tab_item(t[0], t[1], t[2], t[3]) for t in tabs
            ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
            padding=ft.Padding.symmetric(vertical=6),
            bgcolor=ft.Colors.WHITE,
            border=ft.Border.only(top=ft.BorderSide(1, "#E2E8F0")),
            shadow=ft.BoxShadow(spread_radius=0, blur_radius=10, color=ft.Colors.with_opacity(0.05, "#000000"))
        )

    def navigate_to(target):
        nonlocal current_screen, current_tab_index

        # Handle integer tab indexes or string route names
        if isinstance(target, int):
            route_map = {0: "home", 1: "appointments", 2: "scan_lab", 3: "user_profile", 4: "reports"}
            target_route = route_map.get(target, "home")
        else:
            target_route = target

        current_screen = target_route

        # Map active bottom tab index
        if target_route in ["home", "splash"]:
            current_tab_index = 0
        elif target_route in ["appointments", "doctors", "profile", "video_call"]:
            current_tab_index = 1
        elif target_route in ["scan_lab", "reports", "risk_ml"]:
            current_tab_index = 2
        elif target_route in ["user_profile", "medicines"]:
            current_tab_index = 3

        # Route resolution to view builders
        if target_route == "splash":
            animated_switcher.content = build_sanjeevani_splash_screen(page, navigate_to)
            nav_container.visible = False
        elif target_route == "home":
            animated_switcher.content = build_sanjeevani_home_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "doctors":
            animated_switcher.content = build_sanjeevani_doctors_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "profile":
            animated_switcher.content = build_sanjeevani_profile_screen(page, navigate_to)
            nav_container.visible = False
        elif target_route == "appointments":
            animated_switcher.content = build_sanjeevani_appointments_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "video_call":
            animated_switcher.content = build_sanjeevani_video_screen(page, navigate_to)
            nav_container.visible = False
        elif target_route == "medicines":
            animated_switcher.content = build_sanjeevani_medicine_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "scan_lab":
            animated_switcher.content = build_scan_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "reports":
            animated_switcher.content = build_report_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "risk_ml":
            animated_switcher.content = build_risk_screen(page, navigate_to)
            nav_container.visible = True
        elif target_route == "user_profile":
            animated_switcher.content = build_sanjeevani_user_profile_screen(page, navigate_to)
            nav_container.visible = True
        else:
            animated_switcher.content = build_sanjeevani_home_screen(page, navigate_to)
            nav_container.visible = True

        nav_container.content = build_ios_bottom_nav(current_tab_index)
        page.update()

    # Initial screen launch: Home Dashboard
    nav_container.content = build_ios_bottom_nav(0)
    navigate_to("home")

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
