@echo off
rem ==========================================================
rem run_project.bat - Master Startup Script (Windows - Flask)
rem ==========================================================

cd /d "%~dp0"

echo ==========================================================
echo NETFLIX BIG DATA ANALYTICS PLATFORM (FLASK + MONGODB)
echo ==========================================================

echo [1/3] Verifying dependencies...
pip install -r requirements.txt --quiet

echo.
echo [2/3] Executing Data Cleaning Pipeline...
python python\data_cleaning.py

echo.
echo [3/3] Launching Flask Web Application...
python app.py

pause
