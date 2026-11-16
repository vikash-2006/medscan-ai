import subprocess
import time
import sys
import os

def main():
    print("==================================================")
    print("  Launching MedScan AI Suite (Backend + Mobile App)")
    print("==================================================")
    
    # 1. Start FastAPI Backend in background
    backend_proc = subprocess.Popen([
        sys.executable, "-m", "uvicorn", "backend.main:app", 
        "--host", "127.0.0.1", "--port", "8000"
    ])
    print("[*] FastAPI Backend starting on http://127.0.0.1:8000 ...")
    time.sleep(2)  # Give backend a moment to bind port

    # 2. Launch Mobile App
    try:
        from app.main import main as app_main
        import flet as ft
        
        view_mode = ft.AppView.FLET_APP
        if "--web" in sys.argv:
            view_mode = ft.AppView.WEB_BROWSER

        print("[*] Launching Mobile UI...")
        ft.run(app_main, view=view_mode)
    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        print("[*] Shutting down backend...")
        backend_proc.terminate()
        backend_proc.wait()
        print("[*] All stopped cleanly.")

if __name__ == "__main__":
    main()
