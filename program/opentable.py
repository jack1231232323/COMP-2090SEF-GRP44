# open_table.py
import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
from config import *
from UI import style_entry, create_button, fade_in, pulse_button, shake_widget, fade_out
from topup import TopUpDialog

def _font(font_spec):
    """Convert font tuple to tkinter Font object if needed."""
    if isinstance(font_spec, tuple):
        return font.Font(family=font_spec[0], size=int(font_spec[1]))
    return font_spec

class OpenTableDialog(tk.Toplevel):
    def __init__(self, master, storage, username, table_id, on_done):
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.table_id = table_id
        self.on_done = on_done
        self.hours_var = tk.IntVar(value=1)

        self.title(f"Open Table {table_id}")
        self.configure(bg=BG_ROOT)

        self.resizable(False, False)
        self.grab_set()
        self.geometry("380x600")
        self._center()

        self._build()
        
        # Fade in animation
        self.after(100, lambda: fade_in(self))

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        # Main container
        main = tk.Frame(self, bg=BG_ROOT, padx=15, pady=15)
        main.pack(fill="both", expand=True)

        # Title
        tk.Label(main, text=f"Table {self.table_id}", 
                font=("Segoe UI", 18, "bold"),
                fg=ACCENT, bg=BG_ROOT).pack(pady=(0, 10))

        # User info
        user = self.storage.get_user(self.username)
        
        # Check if user exists
        if not user:
            messagebox.showerror("Error", "User not found!")
            self.destroy()
            return
        
        # Balance display
        balance_frame = tk.Frame(main, bg=BG_CARD, highlightthickness=2, 
                                highlightbackground=SUCCESS, relief="solid")
        balance_frame.pack(fill="x", pady=5, ipady=3)
        
        tk.Label(balance_frame, text="YOUR BALANCE", font=("Segoe UI", 9, "bold"),
                fg=TEXT_DIM, bg=BG_CARD).pack()
        
        self.balance_lbl = tk.Label(balance_frame, text=f"${user.balance:.2f}",
                                    font=("Segoe UI", 18, "bold"), fg=SUCCESS, bg=BG_CARD)
        self.balance_lbl.pack()

        # Duration selection
        tk.Label(main, text="SELECT DURATION", font=("Segoe UI", 11, "bold"),
                fg=TEXT, bg=BG_ROOT).pack(anchor="w", pady=(8, 5))

        # Radio buttons for hours
        radio_frame = tk.Frame(main, bg=BG_ROOT)
        radio_frame.pack(fill="x", pady=2)

        for h in [1, 2, 3, 4]:
            cost = h * RATE_PER_HOUR
            rb = tk.Radiobutton(
                radio_frame,
                text=f"{h}h  —  ${cost}",  
                variable=self.hours_var,
                value=h,
                bg=BG_ROOT, fg=TEXT,
                selectcolor=BG_CARD,
                activebackground=BG_ROOT,
                activeforeground=ACCENT,
                font=("Segoe UI", 10)
            )
            rb.pack(anchor="w", pady=1)

        # Total cost display
        cost_frame = tk.Frame(main, bg=BG_CARD, highlightthickness=2, 
                             highlightbackground=ACCENT, relief="solid")
        cost_frame.pack(fill="x", pady=8, ipady=3)
        
        tk.Label(cost_frame, text="TOTAL COST", font=("Segoe UI", 9, "bold"),
                fg=TEXT_DIM, bg=BG_CARD).pack()
        
        # Calculate initial cost
        initial_cost = self.hours_var.get() * RATE_PER_HOUR
        self.cost_lbl = tk.Label(cost_frame, text=f"${initial_cost}", 
                                font=("Segoe UI", 18, "bold"),
                                fg=ACCENT, bg=BG_CARD)
        self.cost_lbl.pack()

        # Message label
        self.msg_lbl = tk.Label(main, text="", fg=ERROR, bg=BG_ROOT, 
                               font=("Segoe UI", 9), wraplength=350, height=2)
        self.msg_lbl.pack(pady=5)

        # BUTTON FRAME - for better organization
        button_frame = tk.Frame(main, bg=BG_ROOT)
        button_frame.pack(fill="x", pady=10)

        # CONFIRM BUTTON - Smaller
        self.confirm_btn = tk.Button(
            button_frame, 
            text="✓ CONFIRM", 
            command=self._confirm,
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
        self.confirm_btn.pack(pady=2)

        # TOP UP BUTTON - Smaller
        self.topup_btn = tk.Button(
            button_frame, 
            text="💰 TOP UP", 
            command=self._topup,
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
        self.topup_btn.pack(pady=2)

        # CANCEL BUTTON - Smaller
        self.cancel_btn = tk.Button(
            button_frame, 
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
        self.cancel_btn.pack(pady=2)

        # Additional space at the bottom
        tk.Label(main, text="", bg=BG_ROOT, height=1).pack()

        # Hover effects
        self.confirm_btn.bind("<Enter>", lambda e: self.confirm_btn.config(bg="#2ea44f"))
        self.confirm_btn.bind("<Leave>", lambda e: self.confirm_btn.config(bg=SUCCESS))
        
        self.topup_btn.bind("<Enter>", lambda e: self.topup_btn.config(bg="#0077ed"))
        self.topup_btn.bind("<Leave>", lambda e: self.topup_btn.config(bg=ACCENT))
        
        self.cancel_btn.bind("<Enter>", lambda e: self.cancel_btn.config(bg="#d32f2f"))
        self.cancel_btn.bind("<Leave>", lambda e: self.cancel_btn.config(bg=ERROR))

        # Bind the hours variable to update cost
        self.hours_var.trace("w", lambda *args: self._update_cost())

    def _update_cost(self):
        """Update the total cost display"""
        cost = self.hours_var.get() * RATE_PER_HOUR
        self.cost_lbl.config(text=f"${cost:.2f}") 

    def _confirm(self):
        """Confirm table opening"""
        hours = self.hours_var.get()
        cost = hours * RATE_PER_HOUR
        
        # Double-check balance
        user = self.storage.get_user(self.username)
        if not user:
            self.msg_lbl.config(text="❌ User not found!", fg=ERROR)
            return
            
        if user.balance < cost:
            self.msg_lbl.config(text=f"❌ Need ${cost}, you have ${user.balance}", fg=ERROR)
            shake_widget(self.msg_lbl)
            return
            
        ok, msg = self.storage.open_table(self.table_id, self.username, hours)
        if ok:
            self.msg_lbl.config(text="✅ Table opened!", fg=SUCCESS)
            # Visual feedback
            self.confirm_btn.config(text="✓ OPENED!", bg="#2ea44f", state="disabled")
            # Call on_done to refresh dashboard
            self.on_done()
            # Close after 1 second
            self.after(1000, self.destroy)
        else:
            self.msg_lbl.config(text="❌ " + msg)
            shake_widget(self.msg_lbl)

    def _topup(self):
        """Open top up dialog"""
        TopUpDialog(self, self.storage, self.username, self._refresh_balance)

    def _refresh_balance(self):
        """Refresh balance after top up"""
        user = self.storage.get_user(self.username)
        if user:
            self.balance_lbl.config(text=f"${user.balance:.2f}")
            self.msg_lbl.config(text="✅ Funds added!", fg=SUCCESS)
            pulse_button(self.confirm_btn)