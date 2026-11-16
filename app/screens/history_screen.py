import flet as ft
from app.state import state

def build_history_screen(page: ft.Page, navigate_to) -> ft.Control:
    data = state.load_history()
    reports = data.get("reports", [])
    risk_checks = data.get("risk_assessments", [])

    report_tiles = []
    if not reports:
        report_tiles.append(
            ft.Text("No saved reports found yet. Scan a report in the Scanner tab to save history.",
                    size=12, color=ft.Colors.GREY_600)
        )
    else:
        for r in reports:
            bio_cnt = len(r.get("biomarkers", []))
            expl = r.get("explanation", {})
            urg = expl.get("urgency_level", "Normal")
            badge_color = ft.Colors.GREEN_700 if urg == "Normal" else (ft.Colors.RED_700 if urg == "High Priority" else ft.Colors.AMBER_700)

            def select_report(e, item=r):
                state.current_report_title = item.get("title", "Medical Report")
                state.current_scan_data = {
                    "raw_text": item.get("raw_text", ""),
                    "biomarkers": item.get("biomarkers", []),
                    "markers_count": len(item.get("biomarkers", [])),
                    "abnormal_count": sum(1 for m in item.get("biomarkers", []) if m.get("status") != "NORMAL")
                }
                state.current_explanation = item.get("explanation", {})
                navigate_to(2)

            report_tiles.append(
                ft.Card(
                    elevation=1,
                    content=ft.Container(
                        content=ft.Row([
                            ft.Icon(ft.Icons.DESCRIPTION_ROUNDED, color=ft.Colors.TEAL_700),
                            ft.Column([
                                ft.Text(r.get("title", "Report"), size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(f"{bio_cnt} Biomarkers | Date: {r.get('created_at', '')[:10]}", size=11, color=ft.Colors.GREY_600),
                            ], expand=True),
                            ft.Container(
                                content=ft.Text(urg, size=11, weight=ft.FontWeight.BOLD, color=badge_color),
                                padding=ft.padding.symmetric(horizontal=8, vertical=4),
                                border_radius=6,
                                bgcolor=ft.Colors.GREY_100
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=12,
                        border_radius=10,
                        ink=True,
                        on_click=select_report
                    )
                )
            )

    risk_tiles = []
    for rc in risk_checks:
        risk_lvl = rc.get("predicted_risk", "Risk")
        col = ft.Colors.GREEN_700 if risk_lvl == "Low Risk" else (ft.Colors.RED_700 if risk_lvl == "High Risk" else ft.Colors.AMBER_700)
        risk_tiles.append(
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.SPEED_ROUNDED, color=col, size=20),
                    ft.Text(f"{rc.get('patient_name', 'Patient')} — {risk_lvl} ({rc.get('risk_probability', 0):.1f}%)", size=12, expand=True),
                    ft.Text(str(rc.get("created_at", ""))[:10], size=11, color=ft.Colors.GREY_500)
                ], spacing=6),
                padding=ft.padding.symmetric(vertical=4)
            )
        )

    return ft.ListView(
        controls=[
            ft.Row([
                ft.Icon(ft.Icons.HISTORY_ROUNDED, color=ft.Colors.TEAL_800),
                ft.Text("Diagnostic History", size=18, weight=ft.FontWeight.BOLD),
            ], spacing=8),
            ft.Text("Past medical scan logs and Sanjeevani risk assessments.", size=12, color=ft.Colors.GREY_600),
            ft.Container(height=8),
            ft.Text("Saved Lab Reports:", size=14, weight=ft.FontWeight.BOLD),
            *report_tiles,
            ft.Container(height=12),
            ft.Text("Past ML Risk Assessments:", size=14, weight=ft.FontWeight.BOLD),
            *(risk_tiles if risk_tiles else [ft.Text("No risk assessments logged yet.", size=12, color=ft.Colors.GREY_600)]),
            ft.Container(height=20)
        ],
        spacing=8,
        padding=16
    )
