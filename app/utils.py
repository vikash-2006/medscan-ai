import flet as ft
from typing import Optional, List

def show_snackbar(page: ft.Page, message: str, bgcolor: Optional[str] = None, duration_ms: int = 3500):
    """
    Cross-version resilient SnackBar dispatcher for Flet 0.20 through 1.1.2+.
    Guarantees no `'Page' object has no attribute 'open'` error.
    """
    if not page:
        return

    try:
        sb = ft.SnackBar(
            content=ft.Text(message, color=ft.Colors.WHITE, size=13, weight=ft.FontWeight.W_500),
            bgcolor=bgcolor or "#2563EB",
            duration=duration_ms
        )

        # 1. Try modern Flet 1.x show_dialog (SnackBar is a DialogControl in Flet 1.1+)
        if hasattr(page, "show_dialog") and callable(page.show_dialog):
            try:
                page.show_dialog(sb)
                return
            except Exception:
                pass

        # 2. Try page.open method if present
        if hasattr(page, "open") and callable(page.open):
            try:
                page.open(sb)
                return
            except Exception:
                pass

        # 3. Try page.overlay fallback
        if hasattr(page, "overlay"):
            if sb not in page.overlay:
                page.overlay.append(sb)
            sb.open = True
            page.update()
            return

        # 4. Try legacy page.snack_bar attribute
        if hasattr(page, "snack_bar"):
            page.snack_bar = sb
            sb.open = True
            page.update()
            return
    except Exception as e:
        print(f"[UI Warning] show_snackbar failed gracefully: {e}")

def show_dialog_modal(page: ft.Page, title: str, content: ft.Control, actions: Optional[List[ft.Control]] = None):
    """
    Displays an AlertDialog safely across any Flet version.
    """
    if not page:
        return

    def close_dlg(e):
        try:
            if hasattr(page, "pop_dialog") and callable(page.pop_dialog):
                page.pop_dialog()
            elif hasattr(page, "close") and callable(page.close):
                page.close(dlg)
            else:
                dlg.open = False
                page.update()
        except Exception:
            pass

    default_actions = actions or [
        ft.TextButton("Close", on_click=close_dlg)
    ]

    dlg = ft.AlertDialog(
        title=ft.Text(title, size=16, weight=ft.FontWeight.BOLD, color="#0F172A"),
        content=content,
        actions=default_actions,
        shape=ft.RoundedRectangleBorder(radius=16),
        bgcolor=ft.Colors.WHITE
    )

    try:
        if hasattr(page, "show_dialog") and callable(page.show_dialog):
            try:
                page.show_dialog(dlg)
            except RuntimeError as e:
                if "Dialog is already opened" in str(e):
                    page.pop_dialog()
                    page.show_dialog(dlg)
                else:
                    raise e
        elif hasattr(page, "open") and callable(page.open):
            page.open(dlg)
        elif hasattr(page, "overlay"):
            page.overlay.append(dlg)
            dlg.open = True
            page.update()
    except Exception as e:
        print(f"[UI Warning] show_dialog_modal failed gracefully: {e}")

def trigger_haptic(page: ft.Page):
    """Safely triggers haptic feedback if supported."""
    try:
        if hasattr(page, "haptic_feedback"):
            page.haptic_feedback()
    except Exception:
        pass
