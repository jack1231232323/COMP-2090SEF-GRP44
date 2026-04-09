import tkinter as tk
from tkinter import messagebox
from config import *
from tabless import TableCard

class Dashboard(tk.Frame):
    def __init__(self, master, storage, cur_user, on_logout):
        tk.Frame.__init__(self, master, bg=bgroot)
        self.storage = storage
        self.cur_user = cur_user
        self.on_logout = on_logout
        self.pack(fill="both", expand=True, padx=24, pady=16)

        top = tk.Frame(self, bg=bgcard, height=50)
        top.pack(fill="x")
        top.pack_propagate(False)
        tk.Label(top, text="Mahjong Tables", font=fontheading, fg=text, bg=bgcard).pack(side="left", padx=20, pady=10)
        self.user_lbl = tk.Label(top, text="", font=fontbody, fg=textdim, bg=bgcard)
        self.user_lbl.pack(side="right", padx=20)
        self.topup_btn = tk.Button(top, text="Top Up", command=self._topup, bg=accent, fg="white", font=fontbtn, width=10, pady=5)
        self.topup_btn.pack(side="right", padx=8)
        tk.Button(top, text="Sign Out", command=self.on_logout, bg=bgactive, fg=textdim, font=fontbtn, width=10, pady=5).pack(side="right", padx=8)
        self._update_user()

        stats = tk.Frame(self, bg=bgcard, pady=10, padx=20)
        stats.pack(fill="x", pady=(0,20))
        tk.Label(stats, text="Active tables: %d / 4" % len(self.storage.bookings), font=fontbody, fg=text, bg=bgcard).pack(side="left", padx=20)

        grid = tk.Frame(self, bg=bgroot)
        grid.pack(fill="both", expand=True)
        self.cards = {}
        for i, tid in enumerate(tableids):
            card = TableCard(grid, tid, self)
            row, col = i//2, i%2
            card.grid(row=row, column=col, padx=14, pady=14, sticky="nsew")
            self.cards[tid] = card
            card.update(self.storage.bookings.get(tid))
        grid.columnconfigure((0,1), weight=1)

    def _update_user(self):
        u = self.storage.get_user(self.cur_user)
        if u:
            new = "%s  •  $%.2f" % (self.cur_user, u.balance)
            self.user_lbl.config(text=new)
            self.user_lbl.config(fg=accent)
            self.after(200, lambda: self.user_lbl.config(fg=text) if self.user_lbl.cget("text") == new else None)

    def refresh(self):
        for tid, card in self.cards.items():
            card.update(self.storage.bookings.get(tid))
        self._update_user()

    def open_table_dialog(self, tid):
        from opentable_dialog import OpenTableDialog
        OpenTableDialog(self.master, self.storage, self.cur_user, tid, self.refresh)

    def close_table(self, tid):
        if not messagebox.askyesno("Confirm", "Close Table %s?" % tid, parent=self.master):
            return
        ok, msg = self.storage.close_table(tid, self.cur_user)
        if ok:
            messagebox.showinfo("Success", msg, parent=self.master)
            self.refresh()
        else:
            messagebox.showerror("Error", msg, parent=self.master)

    def _topup(self):
        from topup_dialog import TopUpDialog
        TopUpDialog(self.master, self.storage, self.cur_user, self.refresh)
