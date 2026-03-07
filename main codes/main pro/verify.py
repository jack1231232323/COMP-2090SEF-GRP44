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
        
        self.transient(master)
        self.grab_set()
        self.focus_set()
        
        self.center(460, 600)
        
        self.bind('<Return>', lambda e: self.do_login())
        
        self.build()
        
        self.protocol("WM_DELETE_WINDOW", self.do_close)
        
        self.after(100, lambda: fade_in(self))

    def center(self, w, h):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def do_close(self):
        self.master.quit()
        self.destroy()

    def build(self):
        c = tk.Frame(self, bg=BG_ROOT, padx=40, pady=32)
        c.pack(expand=True, fill="both")

        tk.Label(c, text="Mahjong Tables", font=FONT_TITLE,
                 fg=ACCENT, bg=BG_ROOT).pack(pady=(0, 8))

        tk.Label(c, text="Welcome! Please sign in or register", 
                font=FONT_HEADING, fg=TEXT_DIM, bg=BG_ROOT).pack(pady=(0, 24))

        card = tk.Frame(c, bg=BG_CARD, padx=32, pady=28)
        card.pack(fill="x")

        tk.Label(card, text="Username", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.u = tk.Entry(card, width=28)
        style_entry(self.u)
        self.u.pack(fill="x", ipady=8, pady=(4, 16))
        self.u.focus_set()

        tk.Label(card, text="Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.p = tk.Entry(card, width=28, show="•")
        style_entry(self.p)
        self.p.pack(fill="x", ipady=8, pady=(4, 16))

        tk.Label(card, text="Confirm Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        self.cp = tk.Entry(card, width=28, show="•")
        style_entry(self.cp)
        self.cp.pack(fill="x", ipady=8, pady=(4, 16))

        self.msg = tk.Label(card, text="", font=FONT_HEADING, fg=ERROR, bg=BG_CARD, wraplength=300)
        self.msg.pack(pady=8)

        bf = tk.Frame(card, bg=BG_CARD)
        bf.pack(fill="x", pady=8)

        self.lb = create_button(bf, "Login", self.do_login, width=12)
        self.lb.pack(side="left", padx=5, expand=True, fill="x")

        self.rb = create_button(bf, "Register", self.do_reg, bg=SUCCESS, fg="white", width=12)
        self.rb.pack(side="right", padx=5, expand=True, fill="x")

        rlf = tk.Frame(card, bg=BG_CARD)
        rlf.pack(fill="x", pady=4)
        
        self.rlb = create_button(
            rlf, 
            "Register & Auto Login", 
            self.do_reg_login, 
            bg=ACCENT, 
            fg="white", 
            width=28
        )
        self.rlb.pack(fill="x")

        sep = tk.Frame(card, height=2, bg=BORDER)
        sep.pack(fill="x", pady=16)

        inf = tk.Frame(card, bg=BG_CARD)
        inf.pack(fill="x")
        
        tk.Label(inf, text="Test Accounts:", font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w")
        
        tf = tk.Frame(inf, bg=BG_CARD)
        tf.pack(fill="x", pady=4)
        
        tk.Label(tf, text="test", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side="left")
        tk.Label(tf, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side="left")
        create_button(tf, "Use this account", lambda: self.fill_test("test", "test123"), 
                     bg=BG_ACTIVE, fg=TEXT, width=10).pack(side="right")
        
        df = tk.Frame(inf, bg=BG_CARD)
        df.pack(fill="x", pady=4)
        
        tk.Label(df, text="demo", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side="left")
        tk.Label(df, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side="left")
        create_button(df, "Use this account", lambda: self.fill_test("demo", "demo123"), 
                     bg=BG_ACTIVE, fg=TEXT, width=10).pack(side="right")

        tk.Label(card, text="Requirements: Username≥2 chars, Password≥4 chars", 
                font=("Segoe UI", 8), fg=TEXT_DIM, bg=BG_CARD).pack(pady=(16, 0))

    def fill_test(self, u, p):
        self.u.delete(0, tk.END)
        self.u.insert(0, u)
        self.p.delete(0, tk.END)
        self.p.insert(0, p)
        self.cp.delete(0, tk.END)
        self.cp.insert(0, p)
        self.set_msg(f"✨ Filled {u} account, click Login", ok=True)
        bounce_effect(self.lb)

    def set_msg(self, txt, ok=False):
        self.msg.config(text=txt, fg=SUCCESS if ok else ERROR)

    def do_login(self):
        u = self.u.get().strip()
        p = self.p.get()
        
        if not u or not p:
            self.set_msg("Please enter username and password")
            shake_widget(self.u if not u else self.p)
            return
            
        ok, msg = self.storage.login(u, p)
        if ok:
            self.set_msg("✅ Login successful!", ok=True)
            self.after(500, lambda: self.close_and_success(u))
        else:
            self.set_msg(msg)
            shake_widget(self.p)
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)
            self.p.focus_set()

    def close_and_success(self, u):
        fade_out(self, on_complete=lambda: self.on_success(u))

    def do_reg(self):
        u = self.u.get().strip()
        p = self.p.get()
        cp = self.cp.get()
        
        if not u or not p or not cp:
            self.set_msg("Please fill all fields")
            return
        
        if p != cp:
            self.set_msg("Passwords do not match")
            shake_widget(self.cp)
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)
            self.p.focus_set()
            return
        
        if len(u) < 2:
            self.set_msg("Username must be at least 2 characters")
            return
        
        if len(p) < 4:
            self.set_msg("Password must be at least 4 characters")
            return

        ok, msg = self.storage.register(u, p)
        if ok:
            self.set_msg(f"✅ Registration successful! Username: {u}", ok=True)
            pulse_button(self.lb)
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)
        else:
            self.set_msg(f"❌ Registration failed: {msg}")
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)

    def do_reg_login(self):
        u = self.u.get().strip()
        p = self.p.get()
        cp = self.cp.get()
        
        if not u or not p or not cp:
            self.set_msg("Please fill all fields")
            return
        
        if p != cp:
            self.set_msg("Passwords do not match")
            shake_widget(self.cp)
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)
            self.p.focus_set()
            return
        
        if len(u) < 2:
            self.set_msg("Username must be at least 2 characters")
            return
        
        if len(p) < 4:
            self.set_msg("Password must be at least 4 characters")
            return

        ok, msg = self.storage.register(u, p)
        if not ok:
            self.set_msg(f"❌ Registration failed: {msg}")
            self.p.delete(0, tk.END)
            self.cp.delete(0, tk.END)
            return
        
        self.destroy()
        self.on_success(u)