import tkinter as tk
from config import *
from UI import style_entry, mk_btn

class AuthWindow(tk.Toplevel):
    def __init__(self, master, storage, on_success):
        super().__init__(master)
        self.storage = storage
        self.on_success = on_success
        self.title("Mahjong Tables - Login/Reg")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.bind('<Return>', lambda e: self._login())
        self.geometry("460x600")
        self._center()
        self._build()
        self.protocol("WM_DELETE_WINDOW", self._close)

    def _center(self):
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 460)//2
        y = (self.winfo_screenheight() - 600)//2
        self.geometry(f"+{x}+{y}")

    def _close(self):
        self.master.quit()
        self.destroy()

    def _build(self):
        main = tk.Frame(self, bg=BG_ROOT, padx=40, pady=32)
        main.pack(expand=True, fill='both')
        tk.Label(main, text="Mahjong Table Manager", font=FONT_TITLE, fg=ACCENT, bg=BG_ROOT).pack(pady=(0,8))
        tk.Label(main, text="Welcome! Sign in or register", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_ROOT).pack(pady=(0,24))

        card = tk.Frame(main, bg=BG_CARD, padx=32, pady=28)
        card.pack(fill='x')

        tk.Label(card, text="Username", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.uname_ent = tk.Entry(card, width=28)
        style_entry(self.uname_ent)
        self.uname_ent.pack(fill='x', ipady=8, pady=(4,16))
        self.uname_ent.focus_set()

        tk.Label(card, text="Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.pw_ent = tk.Entry(card, width=28, show="•")
        style_entry(self.pw_ent)
        self.pw_ent.pack(fill='x', ipady=8, pady=(4,16))

        tk.Label(card, text="Confirm Password", font=FONT_HEADING, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        self.conf_ent = tk.Entry(card, width=28, show="•")
        style_entry(self.conf_ent)
        self.conf_ent.pack(fill='x', ipady=8, pady=(4,16))

        self.msg_lbl = tk.Label(card, text="", font=FONT_HEADING, fg=ERROR, bg=BG_CARD, wraplength=300)
        self.msg_lbl.pack(pady=8)

        btnf = tk.Frame(card, bg=BG_CARD)
        btnf.pack(fill='x', pady=8)
        self.login_btn = mk_btn(btnf, "Login", self._login, width=12)
        self.login_btn.pack(side='left', padx=5, expand=True, fill='x')
        self.reg_btn = mk_btn(btnf, "Register", self._reg, bg=SUCCESS, width=12)
        self.reg_btn.pack(side='right', padx=5, expand=True, fill='x')
        mk_btn(card, "Register & Auto Login", self._reg_login, width=28).pack(fill='x', pady=4)

        tk.Frame(card, height=2, bg=BORDER).pack(fill='x', pady=16)

        info = tk.Frame(card, bg=BG_CARD)
        info.pack(fill='x')
        tk.Label(info, text="Test accounts:", font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).pack(anchor='w')
        f1 = tk.Frame(info, bg=BG_CARD)
        f1.pack(fill='x', pady=4)
        tk.Label(f1, text="test", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side='left')
        tk.Label(f1, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side='left')
        mk_btn(f1, "Use", lambda: self._fill("test","test123"), bg=BG_ACTIVE, width=10).pack(side='right')
        f2 = tk.Frame(info, bg=BG_CARD)
        f2.pack(fill='x', pady=4)
        tk.Label(f2, text="demo", font=FONT_BODY, fg=TEXT, bg=BG_CARD, width=8).pack(side='left')
        tk.Label(f2, text="••••••", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, width=8).pack(side='left')
        mk_btn(f2, "Use", lambda: self._fill("demo","demo123"), bg=BG_ACTIVE, width=10).pack(side='right')

        tk.Label(card, text="Requirements: username≥2, password≥4", font=("Segoe UI",8), fg=TEXT_DIM, bg=BG_CARD).pack(pady=(16,0))

    def _fill(self, u, p):
        self.uname_ent.delete(0, tk.END)
        self.uname_ent.insert(0, u)
        self.pw_ent.delete(0, tk.END)
        self.pw_ent.insert(0, p)
        self.conf_ent.delete(0, tk.END)
        self.conf_ent.insert(0, p)
        self.msg_lbl.config(text=f"Filled {u}", fg=SUCCESS)

    def _set_msg(self, txt, ok=False):
        self.msg_lbl.config(text=txt, fg=SUCCESS if ok else ERROR)

    def _login(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        if not u or not p:
            self._set_msg("Enter username/password")
            return
        ok, msg = self.storage.login(u, p)
        if ok:
            self._set_msg("Login OK!", True)
            self.after(500, lambda: self._done(u))
        else:
            self._set_msg(msg)
            self.pw_ent.delete(0, tk.END)
            self.conf_ent.delete(0, tk.END)

    def _done(self, u):
        self.on_success(u)
        self.destroy()

    def _reg(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        c = self.conf_ent.get()
        if not u or not p or not c:
            self._set_msg("Fill all fields")
            return
        if p != c:
            self._set_msg("Passwords don't match")
            return
        if len(u) < 2:
            self._set_msg("Username too short")
            return
        if len(p) < 4:
            self._set_msg("Password too short")
            return
        ok, msg = self.storage.register(u, p)
        if ok:
            self._set_msg(f"Registered {u}", True)
            self.pw_ent.delete(0, tk.END)
            self.conf_ent.delete(0, tk.END)
        else:
            self._set_msg(f"Reg failed: {msg}")

    def _reg_login(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        c = self.conf_ent.get()
        if not u or not p or not c:
            self._set_msg("Fill all fields")
            return
        if p != c:
            self._set_msg("Passwords don't match")
            return
        if len(u) < 2 or len(p) < 4:
            self._set_msg("Username≥2, password≥4")
            return
        ok, msg = self.storage.register(u, p)
        if not ok:
            self._set_msg(f"Reg failed: {msg}")
            return
        self.destroy()
        self.on_success(u)