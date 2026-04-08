import tkinter as tk
from tkinter import messagebox
from config import *
from UI import mk_btn
from topup import TopUpDialog

class OpenTableDialog(tk.Toplevel):
    def __init__(self, master, storage, username, tid, on_done):
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.tid = tid
        self.on_done = on_done
        self.hours_var = tk.IntVar(value=1)

        self.title(f"Open Table {tid}")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        self.grab_set()
        self.geometry("380x600")
        self._center()
        self._build()

    def _center(self):
        self.update_idletasks()
        w, h = self.winfo_width(), self.winfo_height()
        x = (self.winfo_screenwidth() - w)//2
        y = (self.winfo_screenheight() - h)//2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        main = tk.Frame(self, bg=BG_ROOT, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        tk.Label(main, text=f"Table {self.tid}", font=("Segoe UI",18,"bold"), fg=ACCENT, bg=BG_ROOT).pack(pady=(0,10))

        user = self.storage.get_user(self.username)
        if not user:
            messagebox.showerror("Error", "User not found!")
            self.destroy()
            return

        bal_frame = tk.Frame(main, bg=BG_CARD, highlightthickness=2, highlightbackground=SUCCESS, relief="solid")
        bal_frame.pack(fill="x", pady=5, ipady=3)
        tk.Label(bal_frame, text="YOUR BALANCE", font=("Segoe UI",9,"bold"), fg=TEXT_DIM, bg=BG_CARD).pack()
        self.bal_lbl = tk.Label(bal_frame, text=f"${user.balance:.2f}", font=("Segoe UI",18,"bold"), fg=SUCCESS, bg=BG_CARD)
        self.bal_lbl.pack()

        tk.Label(main, text="SELECT DURATION", font=("Segoe UI",11,"bold"), fg=TEXT, bg=BG_ROOT).pack(anchor="w", pady=(8,5))
        radio_frame = tk.Frame(main, bg=BG_ROOT)
        radio_frame.pack(fill="x", pady=2)
        for h in [1,2,3,4]:
            cost = h * RATE_PER_HOUR
            rb = tk.Radiobutton(radio_frame, text=f"{h}h  —  ${cost}", variable=self.hours_var, value=h,
                                bg=BG_ROOT, fg=TEXT, selectcolor=BG_CARD, activebackground=BG_ROOT,
                                activeforeground=ACCENT, font=("Segoe UI",10))
            rb.pack(anchor="w", pady=1)

        cost_frame = tk.Frame(main, bg=BG_CARD, highlightthickness=2, highlightbackground=ACCENT, relief="solid")
        cost_frame.pack(fill="x", pady=8, ipady=3)
        tk.Label(cost_frame, text="TOTAL COST", font=("Segoe UI",9,"bold"), fg=TEXT_DIM, bg=BG_CARD).pack()
        init_cost = self.hours_var.get() * RATE_PER_HOUR
        self.cost_lbl = tk.Label(cost_frame, text=f"${init_cost}", font=("Segoe UI",18,"bold"), fg=ACCENT, bg=BG_CARD)
        self.cost_lbl.pack()

        self.msg_lbl = tk.Label(main, text="", fg=ERROR, bg=BG_ROOT, font=("Segoe UI",9), wraplength=350, height=2)
        self.msg_lbl.pack(pady=5)

        btn_frame = tk.Frame(main, bg=BG_ROOT)
        btn_frame.pack(fill="x", pady=10)

        self.confirm_btn = tk.Button(btn_frame, text="✓ CONFIRM", command=self._confirm,
                                     bg=SUCCESS, fg="white", font=("Segoe UI",10,"bold"),
                                     height=1, width=12, cursor="hand2", relief="raised", bd=1, pady=4)
        self.confirm_btn.pack(pady=2)

        self.topup_btn = tk.Button(btn_frame, text="💰 TOP UP", command=self._topup,
                                   bg=ACCENT, fg="white", font=("Segoe UI",9,"bold"),
                                   height=1, width=10, cursor="hand2", relief="raised", bd=1, pady=3)
        self.topup_btn.pack(pady=2)

        cancel_btn = tk.Button(btn_frame, text="✕ CANCEL", command=self.destroy,
                               bg=ERROR, fg="white", font=("Segoe UI",9,"bold"),
                               height=1, width=10, cursor="hand2", relief="raised", bd=1, pady=3)
        cancel_btn.pack(pady=2)

        self.hours_var.trace("w", lambda *a: self._update_cost())

    def _update_cost(self):
        c = self.hours_var.get() * RATE_PER_HOUR
        self.cost_lbl.config(text=f"${c:.2f}")

    def _confirm(self):
        hrs = self.hours_var.get()
        cost = hrs * RATE_PER_HOUR
        user = self.storage.get_user(self.username)
        if not user:
            self.msg_lbl.config(text="❌ User not found!", fg=ERROR)
            return
        if user.balance < cost:
            self.msg_lbl.config(text=f"❌ Need ${cost}, you have ${user.balance}", fg=ERROR)
            return
        ok, msg = self.storage.open_table(self.tid, self.username, hrs)
        if ok:
            self.msg_lbl.config(text="✅ Table opened!", fg=SUCCESS)
            self.confirm_btn.config(text="✓ OPENED!", bg="#2ea44f", state="disabled")
            self.on_done()
            self.after(1000, self.destroy)
        else:
            self.msg_lbl.config(text="❌ " + msg)

    def _topup(self):
        TopUpDialog(self, self.storage, self.username, self._refresh_bal)

    def _refresh_bal(self):
        u = self.storage.get_user(self.username)
        if u:
            self.bal_lbl.config(text=f"${u.balance:.2f}")
            self.msg_lbl.config(text="✅ Funds added!", fg=SUCCESS)