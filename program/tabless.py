# table_card.py
import tkinter as tk
from tkinter import ttk
from config import *
from UI import create_button, pulse_button

class TableCard(tk.Frame):
    def __init__(self, parent, table_id, app):
        super().__init__(parent, bg=BG_CARD, highlightthickness=2,
                         highlightbackground=BORDER, padx=18, pady=16)
        self.table_id = table_id
        self.app = app
        self.booking = None
        self._build_base()
        
        # Add hover effect
        self.bind("<Enter>", self._on_card_enter)
        self.bind("<Leave>", self._on_card_leave)

    def _on_card_enter(self, e):
        self.config(highlightbackground=ACCENT, highlightthickness=2)
    
    def _on_card_leave(self, e):
        self.config(highlightbackground=BORDER, highlightthickness=2)

    def _build_base(self):
        hdr = tk.Frame(self, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"Table {self.table_id}", font=FONT_HEADING,
                 fg=TEXT, bg=BG_CARD).pack(side="left")
        self.badge = tk.Label(hdr, text="Available", font=FONT_HEADING,
                              fg=SUCCESS, bg=BG_CARD)
        self.badge.pack(side="right")

        ttk.Separator(self).pack(fill="x", pady=10)

        self.info = tk.Label(self, text="No active booking", font=FONT_BODY,
                             fg=TEXT_DIM, bg=BG_CARD, justify="left")
        self.info.pack(anchor="w", pady=4)

        self.btn = create_button(self, "Open Table", lambda: self.app.open_table_dialog(self.table_id),
                                 bg=SUCCESS, fg="white", width=20)
        self.btn.pack(pady=(12, 0), fill="x")

    def update(self, booking=None):
        """更新卡片狀態 - 修復：正確處理傳入的預訂資料"""
        self.booking = booking
        is_mine = booking and booking.username == self.app.current_user

        if booking:
            self.badge.config(text="🔴 In Use", fg=ERROR)
            self.configure(highlightbackground=ACCENT if is_mine else BORDER)
            self.info.config(
                fg=TEXT,
                text=f"User: {booking.username}\n"
                     f"{booking.hours} hr • ${booking.cost:.2f}\n"
                     f"Ends ≈ {booking.end_time_str}"
            )
            # Flash effect for occupied tables
            self.after(100, lambda: self.badge.config(fg=ERROR))
            
            if is_mine:
                self.btn.config(
                    text="Close Table", bg=ERROR,
                    command=lambda: self.app.close_table(self.table_id)
                )
                def on_enter(e): self.btn.config(bg="#c92a2a")
                def on_leave(e): self.btn.config(bg=ERROR)
                self.btn.bind("<Enter>", on_enter)
                self.btn.bind("<Leave>", on_leave)
            else:
                self.btn.config(text="In Use", bg=BG_ACTIVE,
                                fg=TEXT_DIM, state="disabled")
        else:
            self.badge.config(text="🟢 Available", fg=SUCCESS)
            self.configure(highlightbackground=BORDER)
            self.info.config(fg=TEXT_DIM, text="No active booking")
            self.btn.config(text="Open Table", bg=SUCCESS, fg="white",
                            state="normal",
                            command=lambda: self.app.open_table_dialog(self.table_id))
            def on_enter(e): self.btn.config(bg="#2ea44f")
            def on_leave(e): self.btn.config(bg=SUCCESS)
            self.btn.bind("<Enter>", on_enter)
            self.btn.bind("<Leave>", on_leave)