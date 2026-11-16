import sys
import os
import types
import flet as ft

# ---------------------------------------------------------------------------
# Flet 1.1+ & Android Serious Python Compatibility Shims
# ---------------------------------------------------------------------------

# 1. Register 'app' module alias if running in standalone APK root
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

if "app" not in sys.modules:
    app_mod = types.ModuleType("app")
    app_mod.__path__ = [current_dir]
    app_mod.__file__ = os.path.join(current_dir, "__init__.py")
    sys.modules["app"] = app_mod

# 2. Colors enum legacy aliases (BLACK87 -> BLACK_87, WHITE70 -> WHITE_70, etc.)
if hasattr(ft, "Colors"):
    for _name in list(dir(ft.Colors)):
        if "_" in _name:
            _alias = _name.replace("_", "")
            try:
                setattr(ft.Colors, _alias, getattr(ft.Colors, _name))
            except Exception:
                pass
    ft.colors = ft.Colors

# 3. Class references for controls and geometry
if hasattr(ft, "Padding"):
    ft.padding = ft.Padding
    # Monkeypatch the module 'flet.controls.padding' directly so
    # module 'flet.controls.padding' has no attribute 'symmetric' NEVER occurs!
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

# 4. Chip avatar -> leading compatibility wrapper
if hasattr(ft, "Chip") and not hasattr(ft, "ActionChip"):
    def _ActionChip(**kwargs):
        if "avatar" in kwargs:
            kwargs["leading"] = kwargs.pop("avatar")
        return ft.Chip(**kwargs)
    ft.ActionChip = _ActionChip

# 5. Alignment lowercase aliases
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

# 6. Runner function alias
if not hasattr(ft, "app") and hasattr(ft, "run"):
    ft.app = ft.run
