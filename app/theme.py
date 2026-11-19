"""
Centralized Theme System for MedScan AI.
All UI colors, fonts, and spacing constants in one place.
Supports Light and Dark mode.
"""

class AppTheme:
    """Central theme configuration. Toggle `dark_mode` to switch themes."""
    
    dark_mode = False

    # === Primary Colors ===
    PRIMARY = "#2563EB"
    PRIMARY_DARK = "#1D4ED8"
    SECONDARY = "#EAF4FF"
    SUCCESS = "#22C55E"
    SUCCESS_BG = "#DCFCE7"
    WARNING = "#F59E0B"
    WARNING_BG = "#FEF3C7"
    DANGER = "#DC2626"
    DANGER_BG = "#FEF2F2"
    STAR = "#F59E0B"

    # === Dynamic (Light/Dark aware) ===
    @classmethod
    def bg(cls):
        return "#0F172A" if cls.dark_mode else "#F8FAFC"

    @classmethod
    def card_bg(cls):
        return "#1E293B" if cls.dark_mode else "#FFFFFF"

    @classmethod
    def text_primary(cls):
        return "#F1F5F9" if cls.dark_mode else "#0F172A"

    @classmethod
    def text_secondary(cls):
        return "#94A3B8" if cls.dark_mode else "#64748B"

    @classmethod
    def text_muted(cls):
        return "#64748B" if cls.dark_mode else "#94A3B8"

    @classmethod
    def border(cls):
        return "#334155" if cls.dark_mode else "#E2E8F0"

    @classmethod
    def nav_bg(cls):
        return "#1E293B" if cls.dark_mode else "#FFFFFF"

    @classmethod
    def shadow_color(cls):
        return "rgba(0,0,0,0.2)" if cls.dark_mode else "rgba(0,0,0,0.04)"

    # === Typography ===
    FONT_FAMILY = "Inter"
    HEADING_SIZE = 20
    SUBHEADING_SIZE = 15
    BODY_SIZE = 13
    CAPTION_SIZE = 11
    SMALL_SIZE = 10

    # === Spacing (8px system) ===
    SPACING_XS = 4
    SPACING_SM = 8
    SPACING_MD = 12
    SPACING_LG = 16
    SPACING_XL = 24
    SPACING_XXL = 32

    # === Border Radius ===
    RADIUS_SM = 8
    RADIUS_MD = 14
    RADIUS_LG = 18
    RADIUS_XL = 22
    RADIUS_PILL = 50

    # === Icon Sizes ===
    ICON_SM = 16
    ICON_MD = 20
    ICON_LG = 24
    ICON_XL = 28


# Global instance shortcut
theme = AppTheme
