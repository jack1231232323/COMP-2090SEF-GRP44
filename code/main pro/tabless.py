import tkinter as tk
from tkinter import ttk
from config import *
from UI import mk_btn

class TableCard(tk.Frame):
    def __init__(self, parent, tid, app):
        super().__init__(parent, bg=BG_CARD, highlightthickness=2, highlightbackground=BORDER, padx=18, pady=16)
        self.tid = tid
        self.app = app
        self.booking = None
        self._base()

        self.bind("<Enter>", self._enter)
        self.bind("<Leave>", self._leave)

    def _enter(self, e):
        self.config(highlightbackground=ACCENT, highlightthickness=2)

    def _leave(self, e):
        self.config(highlightbackground=BORDER, highlightthickness=2)

    def _base(self):
        header = tk.Frame(self, bg=BG_CARD)
        header.pack(fill="x")
        tk.Label(header, text=f"Table {self.tid}", font=FONT_HEADING, fg=TEXT, bg=BG_CARD).pack(side="left")
        self.badge = tk.Label(header, text="Available", font=FONT_HEADING, fg=SUCCESS, bg=BG_CARD)
        self.badge.pack(side="right")
        ttk.Separator(self).pack(fill="x", pady=10)
        self.info = tk.Label(self, text="No active booking", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD, justify="left")
        self.info.pack(anchor="w", pady=4)
        self.btn = mk_btn(self, "Open Table", lambda: self.app.open_table_dialog(self.tid), bg=SUCCESS, fg="white", width=20)
        self.btn.pack(pady=(12,0), fill="x")

    def update(self, booking=None):
        self.booking = booking
        mine = booking and booking.username == self.app.cur_user

        if booking:
            self.badge.config(text="🔴 In Use", fg=ERROR)
            self.config(highlightbackground=ACCENT if mine else BORDER)
            self.info.config(fg=TEXT, text=f"User: {booking.username}\n{booking.hours} hr • ${booking.cost:.2f}\nEnds ≈ {booking.end_time_str}")
            if mine:
                self.btn.config(text="Close Table", bg=ERROR, command=lambda: self.app.close_table(self.tid))
                def enter(e): self.btn.config(bg="#c92a2a")
                def leave(e): self.btn.config(bg=ERROR)
                self.btn.bind("<Enter>", enter)
                self.btn.bind("<Leave>", leave)
            else:
                self.btn.config(text="In Use", bg=BG_ACTIVE, fg=TEXT_DIM, state="disabled")
        else:
            self.badge.config(text="🟢 Available", fg=SUCCESS)
            self.config(highlightbackground=BORDER)
            self.info.config(fg=TEXT_DIM, text="No active booking")
            self.btn.config(text="Open Table", bg=SUCCESS, fg="white", state="normal", command=lambda: self.app.open_table_dialog(self.tid))
            def enter(e): self.btn.config(bg="#2ea44f")
            def leave(e): self.btn.config(bg=SUCCESS)
            self.btn.bind("<Enter>", enter)
            self.btn.bind("<Leave>", leave)