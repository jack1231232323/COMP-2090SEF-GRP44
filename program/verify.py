# auth_window.py
import tkinter as tk
from tkinter import messagebox
from UI import style_entry, create_button, fade_in, shake_widget, pulse_button, bounce_effect, fade_out
from config import *

class AuthWindow(tk.Toplevel):
    def __init__(self, master, storage, on_success):
        super().__init__(master)
        self.storage = storage
        self.on_success = on_success

        self.title("Mahjong Tables - Login/Register")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        
        # Set modal window
        self.transient(master)
        self.grab_set()
        self.focus_set()
        
        self._center(460, 600)  # Increased height
        
        # Bind Enter key
        self.bind('<Return>', lambda e: self._login())
        
        self._build_ui()
        
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Fade in animation
        self.after(100, lambda: fade_in(self))

    def _center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _on_close(self):
        self.master.quit()
        self.destroy()

    def _build_ui(self):
        container = tk.Frame(self, bg=BG_ROOT, padx=40, pady=32)
        container.pack(expand=True, fill="both")

        # Title
        tk.Label(container, text="Mahjong Tables", font=FONT_TITLE,
                 fg=ACCENT, bg=BG_ROOT).pack(pady=(0, 8))

        tk.Label(container, text="Welcome! Please sign in or register", 
                font=FONT_HEADING, fg=TEXT_DIM, bg=BG_ROOT).pack(pady=(0, 24))

        # Login card
        card = tk.Frame(container, bg=BG_CARD, padx=32, pady=28)
        card.pack(fill="x")

        # Username
        tk.Label(card, text="Username", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.ent_user = tk.Entry(card, width=28)
        style_entry(self.ent_user)
        self.ent_user.pack(fill="x", ipady=8, pady=(4, 16))
        self.ent_user.focus_set()

        # Password
        tk.Label(card, text="Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.ent_pass = tk.Entry(card, width=28, show="•")
        style_entry(self.ent_pass)
        self.ent_pass.pack(fill="x", ipady=8, pady=(4, 16))

        # Confirm Password (for registration)
        tk.Label(card, text="Confirm Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.ent_confirm = tk.Entry(card, width=28, show="•")
        style_entry(self.ent_confirm)
        self.ent_confirm.pack(fill="x", ipady=8, pady=(4, 16))

        # Message label
        self.lbl_msg = tk.Label(card, text="", font=FONT_HEADING, fg=ERROR, bg=BG_CARD, wraplength=300)
        self.lbl_msg.pack(pady=8)

        # Button frame
        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.pack(fill="x", pady=8)

        # Login button
        self.btn_signin = create_button(btn_frame, "Login", self._login, width=12)
        self.btn_signin.pack(side="left", padx=5, expand=True, fill="x")

        # Register button
        self.btn_register = create_button(btn_frame, "Register", self.do_register, bg=SUCCESS, fg="white", width=12)
        self.btn_register.pack(side="right", padx=5, expand=True, fill="x")

        # Register and login button
        register_login_frame = tk.Frame(card, bg=BG_CARD)
        register_login_frame.pack(fill="x", pady=4)
        
        self.btn_register_login = create_button(
            register_login_frame, 
            "Register & Auto Login", 
            self._register_and_login, 
            bg=ACCENT, 
            fg="white", 
            width=28
        )
        self.btn_register_login.pack(fill="x")

        # Separator
        separator = tk.Frame(card, height=2, bg=BORDER)
        separator.pack(fill="x", pady=16)

        # Display available test accounts
        info_frame = tk.Frame(card, bg=BG_CARD)
        info_frame.pack(fill="x")
        
        tk.Label(info_frame, text="Test Accounts:", font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        
        # test account button
        test_frame = tk.Frame(info_frame, bg=BG_CARD)
        test_frame.pack(fill="x", pady=4)
        
        tk.Label(test_frame, text="test", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side="left")
        tk.Label(test_frame, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side="left")
        create_button(test_frame, "Use this account", lambda: self._fill_test_account("test", "test123"), 
                     bg=BG_ACTIVE, fg=TEXT, width=10).pack(side="right")
        
        # demo account button
        demo_frame = tk.Frame(info_frame, bg=BG_CARD)
        demo_frame.pack(fill="x", pady=4)
        
        tk.Label(demo_frame, text="demo", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side="left")
        tk.Label(demo_frame, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side="left")
        create_button(demo_frame, "Use this account", lambda: self._fill_test_account("demo", "demo123"), 
                     bg=BG_ACTIVE, fg=TEXT, width=10).pack(side="right")

        # Registration requirements
        tk.Label(card, text="Requirements: Username≥2 chars, Password≥4 chars", 
                font=("Segoe UI", 8), fg=TEXT_DIM, bg=BG_CARD).pack(pady=(16, 0))

    def _fill_test_account(self, username, password):
        """Fill test account"""
        self.ent_user.delete(0, tk.END)
        self.ent_user.insert(0, username)
        self.ent_pass.delete(0, tk.END)
        self.ent_pass.insert(0, password)
        self.ent_confirm.delete(0, tk.END)
        self.ent_confirm.insert(0, password)
        self._msg(f"✨ Filled {username} account, click Login", ok=True)
        bounce_effect(self.btn_signin)

    def _msg(self, text, ok=False):
        self.lbl_msg.config(text=text, fg=SUCCESS if ok else ERROR)

    def _login(self):
        """Login function"""
        u = self.ent_user.get().strip()
        p = self.ent_pass.get()
        
        if not u or not p:
            self._msg("Please enter username and password")
            shake_widget(self.ent_user if not u else self.ent_pass)
            return
            
        ok, msg = self.storage.login(u, p)
        if ok:
            self._msg("✅ Login successful!", ok=True)
            self.after(500, lambda: self._close_and_success(u))
        else:
            self._msg(msg)
            shake_widget(self.ent_pass)
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)
            self.ent_pass.focus_set()

    def _close_and_success(self, username):
        """Close with animation and call success"""
        fade_out(self, on_complete=lambda: self.on_success(username))

    def do_register(self):
        """Register function"""
        u = self.ent_user.get().strip()
        p = self.ent_pass.get()
        c = self.ent_confirm.get()
        
        # Validate input
        if not u or not p or not c:
            self._msg("Please fill all fields")
            return
        
        if p != c:
            self._msg("Passwords do not match")
            shake_widget(self.ent_confirm)
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)
            self.ent_pass.focus_set()
            return
        
        if len(u) < 2:
            self._msg("Username must be at least 2 characters")
            return
        
        if len(p) < 4:
            self._msg("Password must be at least 4 characters")
            return

        # Call storage register method
        ok, msg = self.storage.register(u, p)
        if ok:
            self._msg(f"✅ Registration successful! Username: {u}", ok=True)
            pulse_button(self.btn_signin)
            # Clear password fields, keep username
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)
        else:
            self._msg(f"❌ Registration failed: {msg}")
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)

    def _register_and_login(self):
        """Register and auto login"""
        u = self.ent_user.get().strip()
        p = self.ent_pass.get()
        c = self.ent_confirm.get()
        
        # Validate input
        if not u or not p or not c:
            self._msg("Please fill all fields")
            return
        
        if p != c:
            self._msg("Passwords do not match")
            shake_widget(self.ent_confirm)
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)
            self.ent_pass.focus_set()
            return
        
        if len(u) < 2:
            self._msg("Username must be at least 2 characters")
            return
        
        if len(p) < 4:
            self._msg("Password must be at least 4 characters")
            return

        # Register first
        ok, msg = self.storage.register(u, p)
        if not ok:
            self._msg(f"❌ Registration failed: {msg}")
            self.ent_pass.delete(0, tk.END)
            self.ent_confirm.delete(0, tk.END)
            return
        
        # Registration successful, auto login
        self.destroy()
        self.on_success(u)