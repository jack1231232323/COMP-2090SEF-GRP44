import tkinter as tk
from config import *

class AuthWindow(tk.Toplevel):
    def __init__(self, master, storage, on_success):
        tk.Toplevel.__init__(self, master)
        self.storage = storage
        self.on_success = on_success
        self.title("Mahjong Tables - Login/Reg")
        self.configure(bg=bgroot)
        self.resizable(False, False)
        self.transient(master)
        self.grab_set()
        self.bind('<Return>', lambda e: self.login())
        self.geometry("460x600")
        # center
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 460)//2
        y = (self.winfo_screenheight() - 600)//2
        self.geometry("+%d+%d" % (x, y))

        main = tk.Frame(self, bg=bgroot, padx=40, pady=32)
        main.pack(expand=True, fill='both')
        tk.Label(main, text="Mahjong Table Manager", font=fonttitle, fg=accent, bg=bgroot).pack(pady=(0,8))
        tk.Label(main, text="Welcome! Sign in or register", font=fontheading, fg=textdim, bg=bgroot).pack(pady=(0,24))

        card = tk.Frame(main, bg=bgcard, padx=32, pady=28)
        card.pack(fill='x')

        tk.Label(card, text="Username", font=fontheading, fg=textdim, bg=bgcard).pack(anchor='w')
        self.uname_ent = tk.Entry(card, width=28)
        self._style_entry(self.uname_ent)
        self.uname_ent.pack(fill='x', ipady=8, pady=(4,16))
        self.uname_ent.focus_set()

        tk.Label(card, text="Password", font=fontheading, fg=textdim, bg=bgcard).pack(anchor='w')
        self.pw_ent = tk.Entry(card, width=28, show="•")
        self._style_entry(self.pw_ent)
        self.pw_ent.pack(fill='x', ipady=8, pady=(4,16))

        tk.Label(card, text="Confirm Password", font=fontheading, fg=textdim, bg=bgcard).pack(anchor='w')
        self.conf_ent = tk.Entry(card, width=28, show="•")
        self._style_entry(self.conf_ent)
        self.conf_ent.pack(fill='x', ipady=8, pady=(4,16))

        self.msg_lbl = tk.Label(card, text="", font=fontheading, fg=error, bg=bgcard, wraplength=300)
        self.msg_lbl.pack(pady=8)

        btnf = tk.Frame(card, bg=bgcard)
        btnf.pack(fill='x', pady=8)
        self.login_btn = tk.Button(btnf, text="Login", command=self.login, bg=accent, fg="white", font=fontbtn, width=12, pady=5)
        self.login_btn.pack(side='left', padx=5, expand=True, fill='x')
        self.reg_btn = tk.Button(btnf, text="Register", command=self.register, bg=success, fg="white", font=fontbtn, width=12, pady=5)
        self.reg_btn.pack(side='right', padx=5, expand=True, fill='x')
        tk.Button(card, text="Register & Auto Login", command=self.reg_login, bg=accent, fg="white", font=fontbtn, width=28, pady=5).pack(fill='x', pady=4)

        tk.Frame(card, height=2, bg=border).pack(fill='x', pady=16)

        info = tk.Frame(card, bg=bgcard)
        info.pack(fill='x')
        tk.Label(info, text="Test accounts:", font=fontsmall, fg=textdim, bg=bgcard).pack(anchor='w')
        f1 = tk.Frame(info, bg=bgcard)
        f1.pack(fill='x', pady=4)
        tk.Label(f1, text="test", font=fontbody, fg=text, bg=bgcard, width=8).pack(side='left')
        tk.Label(f1, text="••••••", font=fontbody, fg=textdim, bg=bgcard, width=8).pack(side='left')
        tk.Button(f1, text="Use", command=lambda: self.fill_fields("test","test123"), bg=bgactive, fg=text, font=fontsmall, width=10).pack(side='right')
        f2 = tk.Frame(info, bg=bgcard)
        f2.pack(fill='x', pady=4)
        tk.Label(f2, text="demo", font=fontbody, fg=text, bg=bgcard, width=8).pack(side='left')
        tk.Label(f2, text="••••••", font=fontbody, fg=textdim, bg=bgcard, width=8).pack(side='left')
        tk.Button(f2, text="Use", command=lambda: self.fill_fields("demo","demo123"), bg=bgactive, fg=text, font=fontsmall, width=10).pack(side='right')

        tk.Label(card, text="Requirements: username≥2, password≥4", font=("Segoe UI",8), fg=textdim, bg=bgcard).pack(pady=(16,0))

        self.protocol("WM_DELETE_WINDOW", self._close)

    def _style_entry(self, e):
        e.configure(bg=bgcard, fg=text, insertbackground=text,
                    relief="flat", highlightthickness=2, highlightbackground=border,
                    highlightcolor=accent, font=fontbody, bd=0)
        def on_focus_in(ev): e.config(highlightcolor=accent, highlightbackground=accent)
        def on_focus_out(ev): e.config(highlightcolor=border, highlightbackground=border)
        e.bind("<FocusIn>", on_focus_in)
        e.bind("<FocusOut>", on_focus_out)

    def _close(self):
        self.master.quit()
        self.destroy()

    def fill_fields(self, u, p):
        self.uname_ent.delete(0, tk.END)
        self.uname_ent.insert(0, u)
        self.pw_ent.delete(0, tk.END)
        self.pw_ent.insert(0, p)
        self.conf_ent.delete(0, tk.END)
        self.conf_ent.insert(0, p)
        self.msg_lbl.config(text="Filled %s" % u, fg=success)

    def set_msg(self, txt, ok=False):
        self.msg_lbl.config(text=txt, fg=success if ok else error)

    def login(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        if not u or not p:
            self.set_msg("Enter username/password")
            return
        ok, msg = self.storage.login(u, p)
        if ok:
            self.set_msg("Login OK!", True)
            self.after(500, lambda: self._done(u))
        else:
            self.set_msg(msg)
            self.pw_ent.delete(0, tk.END)
            self.conf_ent.delete(0, tk.END)

    def _done(self, u):
        self.on_success(u)
        self.destroy()

    def register(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        c = self.conf_ent.get()
        if not u or not p or not c:
            self.set_msg("Fill all fields")
            return
        if p != c:
            self.set_msg("Passwords don't match")
            return
        if len(u) < 2:
            self.set_msg("Username too short")
            return
        if len(p) < 4:
            self.set_msg("Password too short")
            return
        ok, msg = self.storage.register(u, p)
        if ok:
            self.set_msg("Registered %s" % u, True)
            self.pw_ent.delete(0, tk.END)
            self.conf_ent.delete(0, tk.END)
        else:
            self.set_msg("Reg failed: %s" % msg)

    def reg_login(self):
        u = self.uname_ent.get().strip()
        p = self.pw_ent.get()
        c = self.conf_ent.get()
        if not u or not p or not c:
            self.set_msg("Fill all fields")
            return
        if p != c:
            self.set_msg("Passwords don't match")
            return
        if len(u) < 2 or len(p) < 4:
            self.set_msg("Username≥2, password≥4")
            return
        ok, msg = self.storage.register(u, p)
        if not ok:
            self.set_msg("Reg failed: %s" % msg)
            return
        self.destroy()
        self.on_success(u)