import tkinter as tk
from tkinter import font, messagebox
from config import *
from UI import create_button, fade_in, pulse_button, shake_widget
from topup import TopUpDialog

def _font(fs):
    if isinstance(fs, tuple):
        return font.Font(family=fs[0], size=int(fs[1]))
    return fs

class OpenTableDialog(tk.Toplevel):
    def __init__(self, master, storage, username, tid, on_done):
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.tid = tid
        self.on_done = on_done
        self.hv = tk.IntVar(value=1)

        self.title(f"Open Table {tid}")
        self.configure(bg=BG_ROOT)

        self.resizable(False, False)
        self.grab_set()
        self.geometry("380x600")
        self.center()

        self.do_build()
        
        self.after(100, lambda: fade_in(self))

    def center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def do_build(self):
        main = tk.Frame(self, bg=BG_ROOT, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(main, text=f"Table {self.tid}", 
                font=("Segoe UI", 18, "bold"),
                fg=ACCENT, bg=BG_ROOT).pack(pady=(0, 10))

        u = self.storage.get_user(self.username)
        
        if not u:
            messagebox.showerror("Error", "User not found!")
            self.destroy()
            return
        
        bf = tk.Frame(main, bg=BG_CARD, highlightthickness=2, 
                     highlightbackground=SUCCESS, relief="solid")
        bf.pack(fill="x", pady=5, ipady=3)
        
        tk.Label(bf, text="YOUR BALANCE", font=("Segoe UI", 9, "bold"),
                fg=TEXT_DIM, bg=BG_CARD).pack()
        
        self.bl = tk.Label(bf, text=f"${u.balance:.2f}",
                          font=("Segoe UI", 18, "bold"), fg=SUCCESS, bg=BG_CARD)
        self.bl.pack()

        tk.Label(main, text="SELECT DURATION", font=("Segoe UI", 11, "bold"),
                fg=TEXT, bg=BG_ROOT).pack(anchor="w", pady=(8, 5))

        rf = tk.Frame(main, bg=BG_ROOT)
        rf.pack(fill="x", pady=2)

        for h in [1, 2, 3, 4]:
            c = h * RATE_PER_HOUR
            rb = tk.Radiobutton(
                rf,
                text=f"{h}h  —  ${c}",  
                variable=self.hv,
                value=h,
                bg=BG_ROOT, fg=TEXT,
                selectcolor=BG_CARD,
                activebackground=BG_ROOT,
                activeforeground=ACCENT,
                font=("Segoe UI", 10)
            )
            rb.pack(anchor="w", pady=1)

        cf = tk.Frame(main, bg=BG_CARD, highlightthickness=2, 
                     highlightbackground=ACCENT, relief="solid")
        cf.pack(fill="x", pady=8, ipady=3)
        
        tk.Label(cf, text="TOTAL COST", font=("Segoe UI", 9, "bold"),
                fg=TEXT_DIM, bg=BG_CARD).pack()
        
        ic = self.hv.get() * RATE_PER_HOUR
        self.cl = tk.Label(cf, text=f"${ic}", 
                          font=("Segoe UI", 18, "bold"),
                          fg=ACCENT, bg=BG_CARD)
        self.cl.pack()

        self.ml = tk.Label(main, text="", fg=ERROR, bg=BG_ROOT, 
                          font=("Segoe UI", 9), wraplength=350, height=2)
        self.ml.pack(pady=5)

        bf2 = tk.Frame(main, bg=BG_ROOT)
        bf2.pack(fill="x", pady=10)

        self.cb = tk.Button(
            bf2, 
            text="✓ CONFIRM", 
            command=self.do_confirm,
            bg=SUCCESS, 
            fg="white", 
            font=("Segoe UI", 10, "bold"),
            height=1,
            width=12,
            cursor="hand2",
            relief="raised",
            bd=1,
            pady=4
        )
        self.cb.pack(pady=2)

        self.tb = tk.Button(
            bf2, 
            text="💰 TOP UP", 
            command=self.do_topup,
            bg=ACCENT, 
            fg="white", 
            font=("Segoe UI", 9, "bold"),
            height=1,
            width=10,
            cursor="hand2",
            relief="raised",
            bd=1,
            pady=3
        )
        self.tb.pack(pady=2)

        self.cancel = tk.Button(
            bf2, 
            text="✕ CANCEL", 
            command=self.destroy,
            bg=ERROR, 
            fg="white", 
            font=("Segoe UI", 9, "bold"),
            height=1,
            width=10,
            cursor="hand2",
            relief="raised",
            bd=1,
            pady=3
        )
        self.cancel.pack(pady=2)

        tk.Label(main, text="", bg=BG_ROOT, height=1).pack()

        self.cb.bind("<Enter>", lambda e: self.cb.config(bg="#2ea44f"))
        self.cb.bind("<Leave>", lambda e: self.cb.config(bg=SUCCESS))
        
        self.tb.bind("<Enter>", lambda e: self.tb.config(bg="#0077ed"))
        self.tb.bind("<Leave>", lambda e: self.tb.config(bg=ACCENT))
        
        self.cancel.bind("<Enter>", lambda e: self.cancel.config(bg="#d32f2f"))
        self.cancel.bind("<Leave>", lambda e: self.cancel.config(bg=ERROR))

        self.hv.trace("w", lambda *a: self.upd_cost())

    def upd_cost(self):
        c = self.hv.get() * RATE_PER_HOUR
        self.cl.config(text=f"${c:.2f}") 

    def do_confirm(self):
        h = self.hv.get()
        c = h * RATE_PER_HOUR
        
        u = self.storage.get_user(self.username)
        if not u:
            self.ml.config(text="❌ User not found!", fg=ERROR)
            return
            
        if u.balance < c:
            self.ml.config(text=f"❌ Need ${c}, you have ${u.balance}", fg=ERROR)
            shake_widget(self.ml)
            return
            
        ok, msg = self.storage.open_table(self.tid, self.username, h)
        if ok:
            self.ml.config(text="✅ Table opened!", fg=SUCCESS)
            self.cb.config(text="✓ OPENED!", bg="#2ea44f", state="disabled")
            self.on_done()
            self.after(1000, self.destroy)
        else:
            self.ml.config(text="❌ " + msg)
            shake_widget(self.ml)

    def do_topup(self):
        TopUpDialog(self, self.storage, self.username, self.refresh_bal)

    def refresh_bal(self):
        u = self.storage.get_user(self.username)
        if u:
            self.bl.config(text=f"${u.balance:.2f}")
            self.ml.config(text="✅ Funds added!", fg=SUCCESS)
            pulse_button(self.cb)