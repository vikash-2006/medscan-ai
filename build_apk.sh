#!/bin/bash
# ========================================================
#  MedScan AI - Android APK Generator Script
#  Framework: Python + Flet CLI
# ========================================================

echo "--------------------------------------------------------"
echo "  Building Android APK for MedScan AI"
echo "  Org: com.vikash.medscan | Target: Android ARM64/x86_64"
echo "--------------------------------------------------------"

cd "$(dirname "$0")"

flet build apk \
  --project "MedScan AI" \
  --org "com.vikash.medscan" \
  --product "MedScan AI Health Assistant" \
  --description "AI Medical Diagnostic & OCR Assistant by Vikash Kumawat" \
  app/

echo ""
echo "Build complete! Check the output directory: build/apk/"
