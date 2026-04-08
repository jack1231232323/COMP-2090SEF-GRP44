import tkinter as tk
from tkinter import ttk
from config import *

class TableCard(tk.Frame):
    def __init__(self, parent, tid, app):
        tk.Frame.__init__(self, parent, bg=bgcard, highlightthickness=2, highlightbackground=border, padx=18, pady=16)
        self.tid = tid
        self.app = app
        self.booking = None

        header = tk.Frame(self, bg=bgcard)
        header.pack(fill="x")
        tk.Label(header, text="Table %s" % tid, font=fontheading, fg=text, bg=bgcard).pack(side="left")
        self.badge = tk.Label(header, text="Available", font=fontheading, fg=success, bg=bgcard)
        self.badge.pack(side="right")
        ttk.Separator(self).pack(fill="x", pady=10)
        self.info = tk.Label(self, text="No active booking", font=fontbody, fg=textdim, bg=bgcard, justify="left")
        self.info.pack(anchor="w", pady=4)
        self.btn = tk.Button(self, text="Open Table", command=lambda: self.app.open_table_dialog(self.tid),
                             bg=success, fg="white", font=fontbtn, width=20, pady=5)
        self.btn.pack(pady=(12,0), fill="x")

        self.bind("<Enter>", lambda e: self.config(highlightbackground=accent, highlightthickness=2))
        self.bind("<Leave>", lambda e: self.config(highlightbackground=border, highlightthickness=2))

    def update(self, booking=None):
        self.booking = booking
        mine = booking and booking.username == self.app.cur_user

        if booking:
            self.badge.config(text="🔴 In Use", fg=error)
            self.config(highlightbackground=accent if mine else border)
            txt = "User: %s\n%d hr • $%.2f\nEnds ≈ %s" % (booking.username, booking.hours, booking.cost, booking.end_time_str)
            self.info.config(fg=text, text=txt)
            if mine:
                self.btn.config(text="Close Table", bg=error, command=lambda: self.app.close_table(self.tid))
                self.btn.bind("<Enter>", lambda e: self.btn.config(bg="#c92a2a"))
                self.btn.bind("<Leave>", lambda e: self.btn.config(bg=error))
            else:
                self.btn.config(text="In Use", bg=bgactive, fg=textdim, state="disabled")
        else:
            self.badge.config(text="🟢 Available", fg=success)
            self.config(highlightbackground=border)
            self.info.config(fg=textdim, text="No active booking")
            self.btn.config(text="Open Table", bg=success, fg="white", state="normal", command=lambda: self.app.open_table_dialog(self.tid))
            self.btn.bind("<Enter>", lambda e: self.btn.config(bg="#2ea44f"))
            self.btn.bind("<Leave>", lambda e: self.btn.config(bg=success))
