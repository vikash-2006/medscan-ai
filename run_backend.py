import uvicorn

if __name__ == "__main__":
    print("==================================================")
    print("  Starting MedScan AI & Sanjeevani Diagnostic API")
    print("  FastAPI Server: http://127.0.0.1:8000")
    print("  Interactive Docs: http://127.0.0.1:8000/docs")
    print("==================================================")
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8000, reload=True)
