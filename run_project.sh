#!/usr/bin/env bash
# ==========================================================
# run_project.sh - Master Startup Script (Linux/Mac/WSL - Flask)
# ==========================================================

set -e

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${PROJECT_DIR}"

echo "=========================================================="
echo "NETFLIX BIG DATA ANALYTICS PLATFORM (FLASK + MONGODB)"
echo "=========================================================="

# 1. Check Python dependencies
echo "[1/3] Installing / Verifying Python dependencies..."
pip install -r requirements.txt --quiet

# 2. Run Python Data Cleaning Pipeline
echo "[2/3] Running Python Data Cleaning Pipeline..."
python3 python/data_cleaning.py || python python/data_cleaning.py

# 3. Launch Flask Web Application
echo "[3/3] Launching Flask Web Server at http://127.0.0.1:5000..."
python3 app.py || python app.py
