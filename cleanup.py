#!/usr/bin/env python3
"""
Auto-uninstall helper for cleanup.
Removes installed dependencies.
"""

import subprocess
import sys

def uninstall_dependencies():
    """Uninstall all installed dependencies"""
    print("[*] Uninstalling dependencies...")
    
    dependencies = [
        'cryptography',
        'requests',
        'PySocks'
    ]
    
    for dep in dependencies:
        print(f"[*] Removing {dep}...", end=' ')
        
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'uninstall', '-y', '-q', dep],
                capture_output=True,
                timeout=30
            )
            
            if result.returncode == 0:
                print("✓")
            else:
                print("✗")
        except Exception as e:
            print(f"✗ - {e}")
    
    print("[+] Cleanup complete!")

if __name__ == '__main__':
    uninstall_dependencies()
