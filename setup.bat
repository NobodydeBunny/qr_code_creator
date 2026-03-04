@echo off
REM QR Code Maker - Windows Setup Script

echo =========================================
echo QR Code Maker - Setup
echo =========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo X Python is not installed!
    echo Please install Python 3.8 or higher from https://www.python.org/downloads/
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo. ✓ %PYTHON_VERSION%
echo.

REM Check if pip is installed
pip --version >nul 2>&1
if errorlevel 1 (
    echo X pip is not installed!
    pause
    exit /b 1
)

for /f "tokens=*" %%i in ('pip --version') do set PIP_VERSION=%%i
echo. ✓ %PIP_VERSION%
echo.

REM Install dependencies
echo. Installing dependencies...
echo. This may take a minute...
echo.

pip install qrcode[pil] --break-system-packages

if errorlevel 1 (
    echo.
    echo X Installation failed!
    echo Please try manually:
    echo    pip install qrcode[pil]
    pause
    exit /b 1
) else (
    echo.
    echo. ✓ Installation successful!
    echo.
    echo =========================================
    echo Next Steps:
    echo =========================================
    echo.
    echo 1. To run the GUI:
    echo    python qr_code_maker.py
    echo.
    echo 2. To generate from command line:
    echo    python qr_code_maker.py --text "Hello World" --output my_qr.png
    echo.
    echo =========================================
    pause
)
