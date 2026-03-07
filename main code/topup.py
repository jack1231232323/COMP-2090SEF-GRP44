import tkinter as tk
from UI import style_entry, create_button, fade_in, pulse_button, shake_widget, fade_out
from config import *

class TopUpDialog(tk.Toplevel):
    def __init__(self, master, storage, username, on_success):
        super().__init__(master)
        self.storage = storage
        self.username = username
        self.on_success = on_success

        self.title("Add Funds")
        self.configure(bg=BG_ROOT)
        self.resizable(False, False)
        self.grab_set()
        self.geometry("400x340")
        self._center()

        self._build()
        
        self.after(100, lambda: fade_in(self))

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"+{x}+{y}")

    def _build(self):
        tk.Label(self, text="Add Funds", font=FONT_HEADING, fg=ACCENT, bg=BG_ROOT).pack(pady=20)

        user = self.storage.get_user(self.username)
        tk.Label(self, text=f"Current: ${user.balance:.2f}", font=FONT_BODY, fg=TEXT, bg=BG_ROOT).pack()

        quick_frame = tk.Frame(self, bg=BG_ROOT)
        quick_frame.pack(pady=16)
        for amt in [30, 50, 100, 200]:
            create_button(quick_frame, f"${amt}", lambda a=amt: self._set_amount(a),
                          bg=BG_ACTIVE, fg=TEXT, width=8).pack(side="left", padx=6)

        tk.Label(self, text="Custom amount:", font=(FONT_SMALL[0], int(FONT_SMALL[1])), fg=TEXT_DIM, bg=BG_ROOT).pack(anchor="w", padx=12, pady=(8,4))
        self.ent = tk.Entry(self, width=16, justify="center")
        style_entry(self.ent)
        self.ent.pack(ipady=8)

        self.msg = tk.Label(self, text="", fg=ERROR, bg=BG_ROOT, font=(FONT_SMALL[0], int(FONT_SMALL[1])))
        self.msg.pack(pady=12)

        f = tk.Frame(self, bg=BG_ROOT)
        f.pack(pady=12)
        self.confirm_btn = create_button(f, "Confirm", self._confirm, width=12)
        self.confirm_btn.pack(side="left", padx=8)
        create_button(f, "Cancel", self.destroy, bg=BG_ACTIVE, width=10).pack(side="left", padx=8)

    def _set_amount(self, amt):
        self.ent.delete(0, tk.END)
        self.ent.insert(0, str(amt))
        self.msg.config(text="")
        pulse_button(self.confirm_btn)

    def _confirm(self):
        try:
            amt = float(self.ent.get())
            if amt <= 0:
                raise ValueError
        except:
            self.msg.config(text="❌ Enter valid amount > 0")
            shake_widget(self.ent)
            return

        ok, msg = self.storage.top_up(self.username, amt)
        if ok:
            self.msg.config(text="✅ " + msg, fg=SUCCESS)
            pulse_button(self.confirm_btn)
            self.on_success()
            self.after(1500, self.destroy)
        else:
            self.msg.config(text="❌ " + msg)
            shake_widget(self.ent)