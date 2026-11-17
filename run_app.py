import sys
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass
import app  # Injects Flet 1.1+ compatibility shims & module monkeypatches
import flet as ft
from app.main import main

if __name__ == "__main__":
    print("==================================================")
    print("  Starting MedScan AI Mobile Android Application")
    print("  Framework: Flet (Python + Flutter Engine)")
    print("==================================================")
    
    # Check if user passed --web or --browser
    view_mode = ft.AppView.FLET_APP
    if "--web" in sys.argv or "--browser" in sys.argv:
        view_mode = ft.AppView.WEB_BROWSER

    ft.run(main, view=view_mode)
