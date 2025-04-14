@echo off
echo Creating Python virtual environment...

:: Set UTF-8 encoding
chcp 65001 > nul
set PYTHONIOENCODING=utf-8

:: Check if venv already exists
if exist venv (
    echo Virtual environment already exists.
    echo To recreate it, delete the 'venv' directory first.
    pause
    exit /b
)

:: Create and activate venv
python -m venv venv
if errorlevel 1 (
    echo Failed to create virtual environment!
    echo Please make sure Python 3.9 or higher is installed and in your PATH.
    pause
    exit /b
)

:: Activate venv
call venv\Scripts\activate
if errorlevel 1 (
    echo Failed to activate virtual environment!
    pause
    exit /b
)

:: Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
if errorlevel 1 (
    echo Warning: Failed to upgrade pip, continuing anyway...
)

:: Install dependencies
echo Installing dependencies...
pip install -e . --no-cache-dir
if errorlevel 1 (
    echo Failed to install dependencies!
    echo Please check the error messages above.
    pause
    exit /b
)

echo.
echo Setup complete! You can now use run_app.bat to launch the application.
echo.

pause 