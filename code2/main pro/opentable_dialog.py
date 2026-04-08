import tkinter as tk
from tkinter import messagebox
from config import *
from topup_dialog import TopUpDialog

class OpenTableDialog(tk.Toplevel):
    def __init__(self, master, storage, username, tid, on_done):
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.tid = tid
        self.on_done = on_done
        self.hours_var = tk.IntVar(value=1)
        
        self.title(f"Open Table {tid}")
        self.configure(bg=BG_MAIN)
        self.resizable(False, False)
        self.grab_set()
        self.geometry("380x600")
        self.center()
        
        main = tk.Frame(self, bg=BG_MAIN, padx=15, pady=15)
        main.pack(fill="both", expand=True)
        
        tk.Label(main, text=f"Table {self.tid}", font=("Segoe UI",18,"bold"), fg=ACCENT_COLOR, bg=BG_MAIN).pack(pady=(0,10))
        
        user = self.storage.get_user(self.username)
        if not user:
            messagebox.showerror("Error", "User not found!")
            self.destroy()
            return
        
        # balance display
        bal_frame = tk.Frame(main, bg=CARD_BG, highlightthickness=2, highlightbackground=SUCCESS_COLOR, relief="solid")
        bal_frame.pack(fill="x", pady=5, ipady=3)
        tk.Label(bal_frame, text="YOUR BALANCE", font=("Segoe UI",9,"bold"), fg=DIM_TEXT, bg=CARD_BG).pack()
        self.bal_lbl = tk.Label(bal_frame, text=f"${user.balance:.2f}", font=("Segoe UI",18,"bold"), fg=SUCCESS_COLOR, bg=CARD_BG)
        self.bal_lbl.pack()
        
        # duration radio buttons
        tk.Label(main, text="SELECT DURATION", font=("Segoe UI",11,"bold"), fg=TEXT_COLOR, bg=BG_MAIN).pack(anchor="w", pady=(8,5))
        radio_frame = tk.Frame(main, bg=BG_MAIN)
        radio_frame.pack(fill="x", pady=2)
        for h in [1,2,3,4]:
            cost = h * self.storage.rate
            rb = tk.Radiobutton(radio_frame, text=f"{h}h  —  ${cost}", variable=self.hours_var, value=h,
                                bg=BG_MAIN, fg=TEXT_COLOR, selectcolor=CARD_BG, activebackground=BG_MAIN,
                                activeforeground=ACCENT_COLOR, font=("Segoe UI",10))
            rb.pack(anchor="w", pady=1)
        
        # total cost
        cost_frame = tk.Frame(main, bg=CARD_BG, highlightthickness=2, highlightbackground=ACCENT_COLOR, relief="solid")
        cost_frame.pack(fill="x", pady=8, ipady=3)
        tk.Label(cost_frame, text="TOTAL COST", font=("Segoe UI",9,"bold"), fg=DIM_TEXT, bg=CARD_BG).pack()
        self.cost_lbl = tk.Label(cost_frame, text=f"${self.hours_var.get() * self.storage.rate:.2f}", font=("Segoe UI",18,"bold"), fg=ACCENT_COLOR, bg=CARD_BG)
        self.cost_lbl.pack()
        
        self.msg_lbl = tk.Label(main, text="", fg=ERROR_COLOR, bg=BG_MAIN, font=("Segoe UI",9), wraplength=350, height=2)
        self.msg_lbl.pack(pady=5)
        
        btn_frame = tk.Frame(main, bg=BG_MAIN)
        btn_frame.pack(fill="x", pady=10)
        
        self.confirm_btn = tk.Button(btn_frame, text="✓ CONFIRM", command=self.confirm,
                                     bg=SUCCESS_COLOR, fg="white", font=("Segoe UI",10,"bold"),
                                     height=1, width=12, cursor="hand2", relief="raised", bd=1, pady=4)
        self.confirm_btn.pack(pady=2)
        
        tk.Button(btn_frame, text="💰 TOP UP", command=self.topup,
                  bg=ACCENT_COLOR, fg="white", font=("Segoe UI",9,"bold"),
                  height=1, width=10, cursor="hand2", relief="raised", bd=1, pady=3).pack(pady=2)
        
        tk.Button(btn_frame, text="✕ CANCEL", command=self.destroy,
                  bg=ERROR_COLOR, fg="white", font=("Segoe UI",9,"bold"),
                  height=1, width=10, cursor="hand2", relief="raised", bd=1, pady=3).pack(pady=2)
        
        self.hours_var.trace("w", self.update_cost)
    
    def center(self):
        self.update_idletasks()
        w, h = 380, 600
        x = (self.winfo_screenwidth() - w)//2
        y = (self.winfo_screenheight() - h)//2
        self.geometry(f"+{x}+{y}")
    
    def update_cost(self, *args):
        c = self.hours_var.get() * self.storage.rate
        self.cost_lbl.config(text=f"${c:.2f}")
    
    def confirm(self):
        hrs = self.hours_var.get()
        cost = hrs * self.storage.rate
        user = self.storage.get_user(self.username)
        if not user:
            self.msg_lbl.config(text="❌ User not found!", fg=ERROR_COLOR)
            return
        if user.balance < cost:
            self.msg_lbl.config(text=f"❌ Need ${cost:.2f}, you have ${user.balance:.2f}", fg=ERROR_COLOR)
            return
        ok, msg = self.storage.open_table(self.tid, self.username, hrs)
        if ok:
            self.msg_lbl.config(text="✅ Table opened!", fg=SUCCESS_COLOR)
            self.confirm_btn.config(text="✓ OPENED!", bg="#2ea44f", state="disabled")
            self.on_done()
            self.after(1000, self.destroy)
        else:
            self.msg_lbl.config(text="❌ " + msg)
    
    def topup(self):
        TopUpDialog(self, self.storage, self.username, self.refresh_bal)
    
    def refresh_bal(self):
        u = self.storage.get_user(self.username)
        if u:
            self.bal_lbl.config(text=f"${u.balance:.2f}")
            self.msg_lbl.config(text="✅ Funds added!", fg=SUCCESS_COLOR)