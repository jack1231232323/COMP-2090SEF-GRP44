# dashboard.py
# Jack's part - main dashboard frame and layout
# Choi's part - top bar, user info, refresh, top-up integration
# Guo's part - table cards and dialog triggers

import tkinter as tk
from tkinter import messagebox
from config import *
from UI import create_button, pulse_button
from tabless import TableCard

class Dashboard(tk.Frame):
    def __init__(self, master, storage, cur_user, on_logout):  # Jack
        super().__init__(master, bg=BG_ROOT)
        self.storage = storage
        self.cur_user = cur_user
        self.on_logout = on_logout
        self.pack(fill="both", expand=True, padx=24, pady=16)
        self.top_frame()
        self.content_frame()

    # Choi's top bar
    def top_frame(self):
        top = tk.Frame(self, bg=BG_CARD, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="Mahjong Tables", font=FONT_HEADING, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20, pady=10)

        self.user_info = tk.Label(top, text="", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD)
        self.user_info.pack(side="right", padx=20)

        self.topup_btn = create_button(top, "Top Up", self.do_topup, bg=ACCENT, width=10)
        self.topup_btn.pack(side="right", padx=8)

        create_button(top, "Sign Out", self.on_logout, bg=BG_ACTIVE, fg=TEXT_DIM, width=10).pack(side="right", padx=8)

        self.update_user_display()

    def update_user_display(self):  # Choi
        u = self.storage.get_user(self.cur_user)
        if u:
            old = self.user_info.cget("text")
            new = f"{self.cur_user}  •  ${u.balance:.2f}"
            self.user_info.config(text=new)
            if old != new:
                self.user_info.config(fg=ACCENT)
                self.after(200, lambda: self.user_info.config(fg=TEXT))

    # Guo's table grid
    def content_frame(self):
        stats = tk.Frame(self, bg=BG_CARD, pady=10, padx=20)
        stats.pack(fill="x", pady=(0, 20))
        tk.Label(stats, text=f"Active tables: {len(self.storage.bookings)} / 4",
                 font=FONT_BODY, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20)

        grid = tk.Frame(self, bg=BG_ROOT)
        grid.pack(fill="both", expand=True)

        self.cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = TableCard(grid, tid, self)
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")
            self.cards[tid] = card
            card.update(self.storage.bookings.get(tid))

        grid.columnconfigure((0,1), weight=1)

    def refresh(self):  # Choi
        for tid, card in self.cards.items():
            card.update(self.storage.bookings.get(tid))
        self.update_user_display()

    # Guo's dialog launcher
    def open_table_dialog(self, tid):
        from opentable import OpenTableDialog
        OpenTableDialog(self.master, self.storage, self.cur_user, tid, self.refresh)

    # Guo's close table
    def close_table(self, tid):
        if not messagebox.askyesno("Confirm", f"Close Table {tid}?", parent=self.master):
            return
        ok, msg = self.storage.close_table(tid, self.cur_user)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.master)
            self.refresh()
        else:
            messagebox.showerror("Error", msg, parent=self.master)

    # Choi's top-up
    def do_topup(self):
        from topup import TopUpDialog
        pulse_button(self.topup_btn)
        TopUpDialog(self.master, self.storage, self.cur_user, self.refresh)