import uvicorn
import socket

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

if __name__ == "__main__":
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
    except Exception:
        local_ip = "127.0.0.1"

    print("==================================================")
    print("  Starting MedScan AI & Sanjeevani Diagnostic API")
    print(f"  Local Machine:  http://127.0.0.1:8000")
    print(f"  Phone / Wi-Fi:  http://{local_ip}:8000")
    print(f"  API Docs:       http://{local_ip}:8000/docs")
    print("==================================================")
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
