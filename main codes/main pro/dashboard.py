import tkinter as tk
from tkinter import messagebox
from config import *
from UI import create_button, pulse_button
from tabless import TableCard

class Dashboard(tk.Frame):
    def __init__(self, master, storage, cur_user, on_logout):
        super().__init__(master, bg=BG_ROOT)
        self.storage = storage
        self.cur_user = cur_user
        self.on_logout = on_logout
        self.pack(fill="both", expand=True, padx=24, pady=16)

        self.do_top()
        self.do_content()

    def do_top(self):
        top = tk.Frame(self, bg=BG_CARD, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)

        tk.Label(top, text="Mahjong Tables", font=FONT_HEADING, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20, pady=10)

        self.ui = tk.Label(top, text="", font=FONT_BODY, fg=TEXT_DIM, bg=BG_CARD)
        self.ui.pack(side="right", padx=20)

        self.tb = create_button(top, "Top Up", self.do_topup, bg=ACCENT, width=10)
        self.tb.pack(side="right", padx=8)
        
        create_button(top, "Sign Out", self.on_logout, bg=BG_ACTIVE, fg=TEXT_DIM, width=10).pack(side="right", padx=8)

        self.upd_user()

    def upd_user(self):
        u = self.storage.get_user(self.cur_user)
        if u:
            old = self.ui.cget("text")
            new = f"{self.cur_user}  •  ${u.balance:.2f}"
            self.ui.config(text=new)
            if old != new:
                self.ui.config(fg=ACCENT)
                self.after(200, lambda: self.ui.config(fg=TEXT))

    def do_content(self):
        s = tk.Frame(self, bg=BG_CARD, pady=10, padx=20)
        s.pack(fill="x", pady=(0, 20))

        tk.Label(s, text=f"Active tables: {len(self.storage.bookings)} / 4",
                 font=FONT_BODY, fg=TEXT, bg=BG_CARD).pack(side="left", padx=20)

        g = tk.Frame(self, bg=BG_ROOT)
        g.pack(fill="both", expand=True)

        self.cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = TableCard(g, tid, self)
            card.grid(row=i//2, column=i%2, padx=14, pady=14, sticky="nsew")
            self.cards[tid] = card
            card.update(self.storage.bookings.get(tid))

        g.columnconfigure((0,1), weight=1)

    def refresh(self):
        for tid, card in self.cards.items():
            card.update(self.storage.bookings.get(tid))
        self.upd_user()

    def open_table_dialog(self, tid):
        from opentable import OpenTableDialog
        OpenTableDialog(self.master, self.storage, self.cur_user, tid, self.refresh)

    def close_table(self, tid):
        if not messagebox.askyesno("Confirm", f"Close Table {tid}?", parent=self.master):
            return
        ok, msg = self.storage.close_table(tid, self.cur_user)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.master)
            self.refresh()
        else:
            messagebox.showerror("Error", msg, parent=self.master)

    def do_topup(self):
        from topup import TopUpDialog
        pulse_button(self.tb)
        TopUpDialog(self.master, self.storage, self.cur_user, self.refresh)