import tkinter as tk
from tkinter import ttk
from config import *
from UI import create_button

class TableCard(tk.Frame):
    def __init__(self, parent, tid, app):
        super().__init__(parent, bg=BG_CARD, highlightthickness=2,
                         highlightbackground=BORDER, padx=18, pady=16)
        self.tid = tid
        self.app = app
        self.booking = None
        self.do_base()
        
        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

    def on_enter(self, e):
        self.config(highlightbackground=ACCENT, highlightthickness=2)
    
    def on_leave(self, e):
        self.config(highlightbackground=BORDER, highlightthickness=2)

    def do_base(self):
        hdr = tk.Frame(self, bg=BG_CARD)
        hdr.pack(fill="x")
        tk.Label(hdr, text=f"Table {self.tid}", font=FONT_HEADING,
                 fg=TEXT, bg=BG_CARD).pack(side="left")
        self.badge = tk.Label(hdr, text="Available", font=FONT_HEADING,
                              fg=SUCCESS, bg=BG_CARD)
        self.badge.pack(side="right")

        ttk.Separator(self).pack(fill="x", pady=10)

        self.info = tk.Label(self, text="No active booking", font=FONT_BODY,
                             fg=TEXT_DIM, bg=BG_CARD, justify="left")
        self.info.pack(anchor="w", pady=4)

        self.btn = create_button(self, "Open Table", lambda: self.app.open_table_dialog(self.tid),
                                 bg=SUCCESS, fg="white", width=20)
        self.btn.pack(pady=(12, 0), fill="x")

    def update(self, booking=None):
        self.booking = booking
        mine = booking and booking.username == self.app.cur_user

        if booking:
            self.badge.config(text="🔴 In Use", fg=ERROR)
            self.configure(highlightbackground=ACCENT if mine else BORDER)
            self.info.config(
                fg=TEXT,
                text=f"User: {booking.username}\n"
                     f"{booking.hours} hr • ${booking.cost:.2f}\n"
                     f"Ends ≈ {booking.end_time_str}"
            )
            self.after(100, lambda: self.badge.config(fg=ERROR))
            
            if mine:
                self.btn.config(
                    text="Close Table", bg=ERROR,
                    command=lambda: self.app.close_table(self.tid)
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
                            command=lambda: self.app.open_table_dialog(self.tid))
            def on_enter(e): self.btn.config(bg="#2ea44f")
            def on_leave(e): self.btn.config(bg=SUCCESS)
            self.btn.bind("<Enter>", on_enter)
            self.btn.bind("<Leave>", on_leave)