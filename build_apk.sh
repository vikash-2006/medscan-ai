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
  --project medscan_ai \
  --org com.vikash.medscan \
  --product "MedScan AI" \
  --description "AI Medical Diagnostic & Health Assistant by Vikash Kumawat" \
  --yes \
  -v \
  app/

echo ""
echo "Build complete! Check the output directory: app/build/apk/"
