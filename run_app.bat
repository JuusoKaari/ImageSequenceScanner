@echo off

:: Check if venv exists
if not exist venv (
    echo Virtual environment not found!
    echo Please run setup_venv.bat first to set up the environment.
    pause
    exit /b
)

:: Activate venv and run the app
call venv\Scripts\activate
python run_scanner.py

:: Keep the window open if there's an error
if errorlevel 1 pause 