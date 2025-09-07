@echo off
TITLE Discord Music Bot

ECHO ==================================================
ECHO  Starting Discord Music Bot and Admin Panel
ECHO ==================================================

REM Check for Python
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    ECHO Python is not installed or not in PATH.
    ECHO Please install Python 3.8+ and add it to your PATH.
    pause
    exit /b
)

REM Create a virtual environment if it doesn't exist
IF NOT EXIST .venv (
    ECHO Creating virtual environment...
    python -m venv .venv
)

ECHO Activating virtual environment...
CALL .venv\Scripts\activate.bat

ECHO Installing dependencies from requirements.txt...
pip install -r requirements.txt

ECHO ==================================================
ECHO  Launching Bot and Web Server...
ECHO  Admin Panel will be available at http://localhost:5000
ECHO ==================================================

REM Start the web server in a new window
start "Admin Panel" cmd /c "python web/app.py"

REM Start the Discord bot in the current window
python bot/main.py

pause
