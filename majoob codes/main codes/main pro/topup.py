# topup.py
# Choi's part - top-up dialog UI and amount selection
# Guo's part - custom amount entry and validation
# Jack's part - success callback and window management

import tkinter as tk
from UI import style_entry, create_button, fade_in, pulse_button, shake_widget
from config import *

class TopUpDialog(tk.Toplevel):
    def __init__(self, master, storage, username, on_success):  # Jack
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.on_success = on_success

        self.title("Add Funds")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        self.grab_set()
        self.geometry("400x340")
        self.center()

        self._build()
        self.after(100, lambda: fade_in(self))

    def center(self):  # Jack
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    # Choi's UI
    def _build(self):
        tk.Label(self, text="Add Funds", font=FONT_HEADING, fg=ACCENT, bg=BG_ROOT).pack(pady=20)

        user = self.storage.get_user(self.username)
        tk.Label(self, text=f"Current: ${user.balance:.2f}", font=FONT_BODY, fg=TEXT, bg=BG_ROOT).pack()

        quick_frame = tk.Frame(self, bg=BG_ROOT)
        quick_frame.pack(pady=16)
        # Choi's preset amounts
        for amt in [30,50,100,200]:
            create_button(quick_frame, f"${amt}", lambda a=amt: self.set_amount(a),
                          bg=BG_ACTIVE, fg=TEXT, width=8).pack(side="left", padx=6)

        # Guo's custom entry
        tk.Label(self, text="Custom amount:", font=(FONT_SMALL[0], int(FONT_SMALL[1])), fg=TEXT_DIM, bg=BG_ROOT).pack(anchor="w", padx=12, pady=(8,4))
        self.entry = tk.Entry(self, width=16, justify="center")
        style_entry(self.entry)
        self.entry.pack(ipady=8)

        self.msg = tk.Label(self, text="", fg=ERROR, bg=BG_ROOT, font=(FONT_SMALL[0], int(FONT_SMALL[1])))
        self.msg.pack(pady=12)

        btn_frame = tk.Frame(self, bg=BG_ROOT)
        btn_frame.pack(pady=12)
        self.confirm_btn = create_button(btn_frame, "Confirm", self.do_confirm, width=12)
        self.confirm_btn.pack(side="left", padx=8)
        create_button(btn_frame, "Cancel", self.destroy, bg=BG_ACTIVE, width=10).pack(side="left", padx=8)

    # Choi's preset filler
    def set_amount(self, amt):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(amt))
        self.msg.config(text="")
        pulse_button(self.confirm_btn)

    # Guo's validation and confirm
    def do_confirm(self):
        try:
            amt = float(self.entry.get())
            if amt <= 0:
                raise ValueError
        except:
            self.msg.config(text="❌ Enter valid amount > 0")
            shake_widget(self.entry)
            return

        ok, msg = self.storage.top_up(self.username, amt)
        if ok:
            self.msg.config(text="✅ " + msg, fg=SUCCESS)
            pulse_button(self.confirm_btn)
            self.on_success()
            self.after(1500, self.destroy)
        else:
            self.msg.config(text="❌ " + msg)
            shake_widget(self.entry)