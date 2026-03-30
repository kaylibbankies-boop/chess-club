@echo off
REM Chess Club Flask App Startup Script for Windows

echo.
echo ============================================
echo   Chess Club Flask Application
echo ============================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

echo [1/5] Creating virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created
) else (
    echo Virtual environment already exists
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate

echo [3/5] Installing dependencies...
pip install -r requirements.txt --quiet

echo [4/5] Checking configuration...
if not exist .env (
    echo Copying .env.example to .env
    copy .env.example .env >nul
)

echo [5/5] Starting Flask server...
echo.
echo ============================================
echo Server starting at: http://localhost:5000
echo Press Ctrl+C to stop
echo ============================================
echo.

python app.py

pause
