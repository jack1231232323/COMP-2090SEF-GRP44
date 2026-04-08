# verify.py
# Choi's part - authentication window UI and logic
# Guo's part - test account filler and animations integration
# Jack's part - window centering and close handling

import tkinter as tk
from config import *
from UI import style_entry, create_button, fade_in, shake_widget, pulse_button, fade_out

class AuthWindow(tk.Toplevel):
    def __init__(self, master, storage, on_success):  # Jack
        super().__init__(master)
        self.storage = storage
        self.on_success = on_success

        self.title("Mahjong Tables - Login / Register")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.bind('<Return>', lambda e: self.do_login())
        self.geometry("460x600")
        self.center()
        self.build()
        self.protocol("WM_DELETE_WINDOW", self.do_close)
        self.after(100, lambda: fade_in(self))

    def center(self):  # Jack
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 460) // 2
        y = (self.winfo_screenheight() - 600) // 2
        self.geometry(f"+{x}+{y}")

    def do_close(self):  # Jack
        self.master.quit()
        self.destroy()

    def build(self):  # Choi
        main = tk.Frame(self, bg=BG_ROOT, padx=40, pady=32)
        main.pack(expand=True, fill='both')

        tk.Label(main, text="Mahjong Table Management", font=FONT_TITLE, fg=ACCENT, bg=BG_ROOT).pack(pady=(0,8))
        tk.Label(main, text="Welcome! Please sign in or register", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_ROOT).pack(pady=(0,24))

        card = tk.Frame(main, bg=BG_CARD, padx=32, pady=28)
        card.pack(fill='x')

        tk.Label(card, text="Username", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.username_entry = tk.Entry(card, width=28)
        style_entry(self.username_entry)
        self.username_entry.pack(fill='x', ipady=8, pady=(4,16))
        self.username_entry.focus_set()

        tk.Label(card, text="Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.password_entry = tk.Entry(card, width=28, show="•")
        style_entry(self.password_entry)
        self.password_entry.pack(fill='x', ipady=8, pady=(4,16))

        tk.Label(card, text="Confirm Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.confirm_entry = tk.Entry(card, width=28, show="•")
        style_entry(self.confirm_entry)
        self.confirm_entry.pack(fill='x', ipady=8, pady=(4,16))

        self.msg_label = tk.Label(card, text="", font=FONT_HEADING, fg=ERROR, bg=BG_CARD, wraplength=300)
        self.msg_label.pack(pady=8)

        btn_frame = tk.Frame(card, bg=BG_CARD)
        btn_frame.pack(fill='x', pady=8)

        self.login_btn = create_button(btn_frame, "Login", self.do_login, width=12)
        self.login_btn.pack(side='left', padx=5, expand=True, fill='x')

        self.reg_btn = create_button(btn_frame, "Register", self.do_reg, bg=SUCCESS, width=12)
        self.reg_btn.pack(side='right', padx=5, expand=True, fill='x')

        self.reglogin_btn = create_button(card, "Register & Auto Login", self.do_reg_login, width=28)
        self.reglogin_btn.pack(fill='x', pady=4)

        sep = tk.Frame(card, height=2, bg=BORDER)
        sep.pack(fill='x', pady=16)

        info_frame = tk.Frame(card, bg=BG_CARD)
        info_frame.pack(fill='x')
        tk.Label(info_frame, text="Test accounts:", font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')

        # Guo's test account filler
        f1 = tk.Frame(info_frame, bg=BG_CARD)
        f1.pack(fill='x', pady=4)
        tk.Label(f1, text="test", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side='left')
        tk.Label(f1, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side='left')
        create_button(f1, "Use this", lambda: self.fill_test("test","test123"), bg=BG_ACTIVE, width=10).pack(side='right')

        f2 = tk.Frame(info_frame, bg=BG_CARD)
        f2.pack(fill='x', pady=4)
        tk.Label(f2, text="demo", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side='left')
        tk.Label(f2, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side='left')
        create_button(f2, "Use this", lambda: self.fill_test("demo","demo123"), bg=BG_ACTIVE, width=10).pack(side='right')

        tk.Label(card, text="Requirements: Username≥2 chars, Password≥4 chars", font=("Segoe UI",8), fg=TEXT_DIM, bg=BG_CARD).pack(pady=(16,0))

    # Guo's fill_test
    def fill_test(self, u, p):
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, u)
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, p)
        self.confirm_entry.delete(0, tk.END)
        self.confirm_entry.insert(0, p)
        self.msg_label.config(text=f"Filled {u} account", fg=SUCCESS)

    def set_msg(self, txt, ok=False):
        self.msg_label.config(text=txt, fg=SUCCESS if ok else ERROR)

    # Choi's login logic
    def do_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get()
        if not u or not p:
            self.set_msg("Please enter username and password")
            return
        ok, msg = self.storage.login(u, p)
        if ok:
            self.set_msg("Login successful!", ok=True)
            self.after(500, lambda: self._close_and_success(u))
        else:
            self.set_msg(msg)
            shake_widget(self.password_entry)
            self.password_entry.delete(0, tk.END)
            self.confirm_entry.delete(0, tk.END)

    def _close_and_success(self, u):  # Jack
        fade_out(self, lambda: self.on_success(u))

    # Choi's registration
    def do_reg(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get()
        cp = self.confirm_entry.get()
        if not u or not p or not cp:
            self.set_msg("Please fill all fields")
            return
        if p != cp:
            self.set_msg("Passwords do not match")
            shake_widget(self.confirm_entry)
            return
        if len(u) < 2:
            self.set_msg("Username too short")
            return
        if len(p) < 4:
            self.set_msg("Password too short")
            return
        ok, msg = self.storage.register(u, p)
        if ok:
            self.set_msg(f"Registration successful: {u}", ok=True)
            pulse_button(self.login_btn)
            self.password_entry.delete(0, tk.END)
            self.confirm_entry.delete(0, tk.END)
        else:
            self.set_msg(f"Registration failed: {msg}")

    # Guo's reg+login
    def do_reg_login(self):
        u = self.username_entry.get().strip()
        p = self.password_entry.get()
        cp = self.confirm_entry.get()
        if not u or not p or not cp:
            self.set_msg("Please fill all fields")
            return
        if p != cp:
            self.set_msg("Passwords do not match")
            return
        if len(u) < 2 or len(p) < 4:
            self.set_msg("Username≥2, Password≥4")
            return
        ok, msg = self.storage.register(u, p)
        if not ok:
            self.set_msg(f"Registration failed: {msg}")
            return
        self.destroy()
        self.on_success(u)