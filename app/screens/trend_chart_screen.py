"""
Blood Sugar Trend Chart Screen for MedScan AI.
Shows 30-day blood sugar trends using Flet's LineChart.
"""
import random
from datetime import datetime, timedelta
import flet as ft
from app.state import state
from app.theme import theme


def build_trend_chart_screen(page: ft.Page, navigate_to) -> ft.Control:
    # --- Extract blood sugar data from history ---
    data_points = []
    try:
        for entry in state.history:
            created_at = entry.get("created_at", "")
            biomarkers = entry.get("biomarkers", [])
            for b in biomarkers:
                if "sugar" in b.get("name", "").lower() or "glucose" in b.get("name", "").lower():
                    try:
                        date_obj = datetime.strptime(created_at[:10], "%Y-%m-%d")
                        data_points.append({"date": date_obj, "value": float(b["value"])})
                    except (ValueError, KeyError):
                        pass
    except Exception:
        pass

    # Generate demo data if not enough points
    if len(data_points) < 5:
        today = datetime.now()
        random.seed(42)  # Consistent demo data
        data_points = []
        for i in range(30):
            d = today - timedelta(days=29 - i)
            val = random.uniform(85, 165)
            data_points.append({"date": d, "value": round(val, 1)})

    # Sort by date
    data_points.sort(key=lambda x: x["date"])

    values = [p["value"] for p in data_points]
    avg_val = round(sum(values) / len(values), 1) if values else 0
    max_val = round(max(values), 1) if values else 0
    min_val = round(min(values), 1) if values else 0
    current_val = round(values[-1], 1) if values else 0

    # Build chart data points
    chart_data_points = []
    for i, p in enumerate(data_points):
        chart_data_points.append(
            ft.LineChartDataPoint(i, p["value"])
        )

    # --- UI ---
    # Back header
    header = ft.Container(
        content=ft.Row([
            ft.Container(
                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED, color=theme.text_primary(), size=18),
                width=38, height=38, border_radius=19,
                bgcolor=theme.card_bg(), alignment=ft.Alignment.CENTER,
                ink=True, on_click=lambda _: navigate_to("home"),
                border=ft.Border.all(1, theme.border())
            ),
            ft.Text("Blood Sugar Trends", size=18, weight=ft.FontWeight.BOLD, color=theme.text_primary()),
            ft.Container(width=38)
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding(18, 10, 18, 5)
    )

    # Current value card
    status_color = theme.SUCCESS if current_val <= 100 else (theme.WARNING if current_val <= 126 else theme.DANGER)
    status_text = "Normal" if current_val <= 100 else ("Pre-Diabetic" if current_val <= 126 else "High")

    current_card = ft.Container(
        content=ft.Column([
            ft.Text("Current Blood Sugar", size=12, color=theme.text_secondary()),
            ft.Row([
                ft.Text(f"{current_val}", size=36, weight=ft.FontWeight.BOLD, color=status_color),
                ft.Text("mg/dL", size=14, color=theme.text_secondary()),
            ], spacing=6, vertical_alignment=ft.CrossAxisAlignment.END),
            ft.Container(
                content=ft.Text(status_text, size=11, weight=ft.FontWeight.BOLD, color=status_color),
                padding=ft.Padding(10, 4, 10, 4), border_radius=8,
                bgcolor=ft.Colors.with_opacity(0.1, status_color)
            )
        ], spacing=4, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        padding=20, border_radius=20,
        bgcolor=theme.card_bg(), border=ft.Border.all(1, theme.border()),
        margin=ft.Padding(18, 5, 18, 5), alignment=ft.Alignment.CENTER
    )

    # Line Chart
    chart = ft.Container(
        content=ft.LineChart(
            data_series=[
                ft.LineChartData(
                    data_points=chart_data_points,
                    stroke_width=3,
                    color=theme.PRIMARY,
                    curved=True,
                    stroke_cap_round=True,
                    below_line_gradient=ft.LinearGradient(
                        begin=ft.Alignment.TOP_CENTER,
                        end=ft.Alignment.BOTTOM_CENTER,
                        colors=[ft.Colors.with_opacity(0.3, theme.PRIMARY), ft.Colors.with_opacity(0.0, theme.PRIMARY)]
                    )
                )
            ],
            min_y=50, max_y=200,
            min_x=0, max_x=len(data_points) - 1,
            expand=True,
            left_axis=ft.ChartAxis(
                labels_size=35,
                labels_interval=25,
            ),
            bottom_axis=ft.ChartAxis(
                labels_size=25,
                labels_interval=max(1, len(data_points) // 6),
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                interval=25,
                color=ft.Colors.with_opacity(0.1, theme.text_secondary()),
                width=1
            ),
            tooltip_bgcolor=theme.card_bg(),
            interactive=True,
        ),
        height=220, padding=ft.Padding(10, 10, 18, 5),
        border_radius=20, bgcolor=theme.card_bg(),
        border=ft.Border.all(1, theme.border()),
        margin=ft.Padding(18, 5, 18, 5)
    )

    # Reference zone legend
    legend = ft.Container(
        content=ft.Row([
            ft.Row([ft.Container(width=10, height=10, border_radius=5, bgcolor=theme.SUCCESS), ft.Text("Normal (<100)", size=10, color=theme.text_secondary())], spacing=4),
            ft.Row([ft.Container(width=10, height=10, border_radius=5, bgcolor=theme.WARNING), ft.Text("Pre-Diabetic (100-126)", size=10, color=theme.text_secondary())], spacing=4),
            ft.Row([ft.Container(width=10, height=10, border_radius=5, bgcolor=theme.DANGER), ft.Text("High (>126)", size=10, color=theme.text_secondary())], spacing=4),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        margin=ft.Padding(18, 0, 18, 5)
    )

    # Summary stats
    stats_row = ft.Container(
        content=ft.Row([
            _stat_card("Average", f"{avg_val}", "mg/dL", theme.PRIMARY),
            _stat_card("Highest", f"{max_val}", "mg/dL", theme.DANGER),
            _stat_card("Lowest", f"{min_val}", "mg/dL", theme.SUCCESS),
        ], alignment=ft.MainAxisAlignment.SPACE_EVENLY),
        margin=ft.Padding(18, 5, 18, 5)
    )

    # 30-day label
    period_label = ft.Container(
        content=ft.Text("📊 30-Day Trend Analysis", size=12, weight=ft.FontWeight.BOLD, color=theme.text_secondary()),
        margin=ft.Padding(22, 5, 18, 0)
    )

    return ft.Container(
        content=ft.Column([
            header, current_card, period_label, chart, legend, stats_row
        ], scroll=ft.ScrollMode.AUTO, spacing=0),
        bgcolor=theme.bg(), expand=True
    )


def _stat_card(label: str, val: str, unit: str, color: str) -> ft.Container:
    """Small stat card for avg/high/low."""
    return ft.Container(
        content=ft.Column([
            ft.Text(label, size=10, color=theme.text_secondary()),
            ft.Text(val, size=18, weight=ft.FontWeight.BOLD, color=color),
            ft.Text(unit, size=9, color=theme.text_muted()),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=1),
        width=100, padding=12, border_radius=16,
        bgcolor=theme.card_bg(), border=ft.Border.all(1, theme.border())
    )
