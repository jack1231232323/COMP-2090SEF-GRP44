# dashboard.py
import tkinter as tk
from tkinter import messagebox
from config import *
from UI import create_button, pulse_button
from tabless import TableCard

class Dashboard(tk.Frame):
    def __init__(self, master, storage, current_user, on_logout):
        super().__init__(master, bg=BG_ROOT)
        self.storage = storage
        self.current_user = current_user
        self.on_logout = on_logout
        self.pack(fill="both", expand=True, padx=24, pady=16)

        self._build_top()
        self._build_content()

    def _build_top(self):
        top = tk.Frame(self, bg=BG_CARD, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="Mahjong Tables", font=FONT_HEADING, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20, pady=10)

        self.user_info = tk.Label(top, text="", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD)
        self.user_info.pack(side="right", padx=20)

        self.topup_btn = create_button(top, "Top Up", self._topup, bg=ACCENT, width=10)
        self.topup_btn.pack(side="right", padx=8)
        
        create_button(top, "Sign Out", self.on_logout, bg=BG_ACTIVE, fg=TEXT_DIM, width=10).pack(side="right", padx=8)

        self._update_user_info()

    def _update_user_info(self):
        user = self.storage.get_user(self.current_user)
        if user:
            old_text = self.user_info.cget("text")
            new_text = f"{self.current_user}  •  ${user.balance:.2f}"
            self.user_info.config(text=new_text)
            # Flash effect when balance changes
            if old_text != new_text:
                self.user_info.config(fg=ACCENT)
                self.after(200, lambda: self.user_info.config(fg=TEXT))

    def _build_content(self):
        summary = tk.Frame(self, bg=BG_CARD, pady=10, padx=20)
        summary.pack(fill="x", pady=(0, 20))

        tk.Label(summary, text=f"Active tables: {len(self.storage.bookings)} / 4",
                 font=FONT_BODY, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20)

        grid = tk.Frame(self, bg=BG_ROOT)
        grid.pack(fill="both", expand=True)

        self.cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = TableCard(grid, tid, self)
            card.grid(row=i//2, column=i%2, padx=14, pady=14, sticky="nsew")
            self.cards[tid] = card
            card.update(self.storage.bookings.get(tid))

        grid.columnconfigure((0,1), weight=1)

    def refresh(self):
        for tid, card in self.cards.items():
            card.update(self.storage.bookings.get(tid))
        self._update_user_info()

    def open_table_dialog(self, table_id):
        from opentable import OpenTableDialog
        OpenTableDialog(self.master, self.storage, self.current_user, table_id, self.refresh)

    def close_table(self, table_id):
        if not messagebox.askyesno("Confirm", f"Close Table {table_id}?", parent=self.master):
            return
        ok, msg = self.storage.close_table(table_id, self.current_user)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.master)
            self.refresh()
        else:
            messagebox.showerror("Error", msg, parent=self.master)

    def _topup(self):
        from topup import TopUpDialog
        pulse_button(self.topup_btn)
        TopUpDialog(self.master, self.storage, self.current_user, self.refresh)