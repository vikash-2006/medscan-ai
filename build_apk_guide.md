# 📱 Android APK Build & Deployment Guide for MedScan AI

MedScan AI ko Android phone par install karne aur `.apk` generate karne ke 2 tareeqe hain:

---

## Method 1: GitHub Actions se Cloud me Free APK Banana (Sabse Aasan ⭐)
Agar aapke Mac par Android Studio ya heavy Android SDKs installed nahi hain, toh GitHub Actions cloud me 5 minutes me aapko ready-to-install `.apk` build karke de deta hai.

### Steps:
1. MedScan AI code ko apne GitHub repository me push karein.
2. Project me `.github/workflows/build_apk.yml` file banayein:

```yaml
name: Build Android APK

on:
  push:
    branches: [ main ]
  workflow_dispatch:

jobs:
  build-android:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.11"

      - name: Set up Java
        uses: actions/setup-java@v4
        with:
          distribution: "temurin"
          java-version: "17"

      - name: Set up Flutter
        uses: subosito/flutter-action@v2
        with:
          channel: "stable"

      - name: Install Flet
        run: pip install flet

      - name: Build Android APK
        run: |
          cd app
          flet build apk --project "MedScan AI" --org "com.vikash.medscan"

      - name: Upload APK Artifact
        uses: actions/upload-artifact@v4
        with:
          name: MedScan-AI-Release.apk
          path: app/build/apk/*.apk
```
3. GitHub Actions run hone ke baad **Actions** tab se `MedScan-AI-Release.apk` download karke kisi bhi Android phone me install kar sakte hain!

---

## Method 2: Local Mac Terminal se Buildozer / Flet CLI se APK Banana

### Prerequisites:
- Python 3.10 / 3.11
- Java Development Kit (JDK 17 or 21):
  ```bash
  brew install openjdk@17
  ```
- Android Command Line Tools / SDK:
  ```bash
  brew install --cask android-commandlinetools
  ```

### Build Command:
```bash
# 1. Project directory me jayein
cd MedScan\ AI

# 2. Flet build apk command run karein (app directory specifies the application path)
flet build apk app --project "MedScan AI" --org "com.vikash.medscan" --icon app/assets/app_icon.png
```
Command complete hone par APK aapko `build/apk/` directory me mil jayegi:
```
build/apk/app-release.apk
```

---

## Phone me Install & Test Kaise Karein:

1. **Via USB Cable (ADB):**
   ```bash
   adb install build/apk/app-release.apk
   ```
2. **Via WhatsApp / Google Drive:**
   `.apk` file ko apne Google Drive ya WhatsApp par send karein aur phone me "Install Unknown Apps" permission allow karke install kar lein.

---

## Local Mac par Mobile View Test Kaise Karein:

Bina APK banaye bhi aap Mac screen par pure Android Mobile frame me ise test kar sakte hain:
```bash
# Terminal 1: Backend start karein
python3 run_backend.py

# Terminal 2: Mobile UI start karein
python3 run_app.py
```
Browser mobile mode ke liye:
```bash
python3 run_app.py --web
```
