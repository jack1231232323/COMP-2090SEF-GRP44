import tkinter as tk
from config import *

class TopUpDialog(tk.Toplevel):
    def __init__(self, master, storage, username, on_success):
        tk.Toplevel.__init__(self, master)
        self.storage = storage
        self.username = username
        self.on_success = on_success
        self.title("Add Funds")
        self.configure(bg=bgroot)
        self.resizable(False, False)
        self.grab_set()
        self.geometry("400x340")
        self.update_idletasks()
        w, h = 400, 340
        x = (self.winfo_screenwidth() - w)//2
        y = (self.winfo_screenheight() - h)//2
        self.geometry("+%d+%d" % (x, y))

        tk.Label(self, text="Add Funds", font=fontheading, fg=accent, bg=bgroot).pack(pady=20)
        user = self.storage.get_user(self.username)
        tk.Label(self, text="Current: $%.2f" % user.balance, font=fontbody, fg=text, bg=bgroot).pack()

        quick = tk.Frame(self, bg=bgroot)
        quick.pack(pady=16)
        for amt in [30,50,100,200]:
            btn = tk.Button(quick, text="$%d" % amt, command=lambda a=amt: self.set_amount(a),
                            bg=bgactive, fg=text, font=fontbtn, width=8, pady=5)
            btn.pack(side="left", padx=6)

        tk.Label(self, text="Custom amount:", font=fontsmall, fg=textdim, bg=bgroot).pack(anchor="w", padx=12, pady=(8,4))
        self.entry = tk.Entry(self, width=16, justify="center")
        self._style_entry(self.entry)
        self.entry.pack(ipady=8)

        self.msg = tk.Label(self, text="", fg=error, bg=bgroot, font=fontsmall)
        self.msg.pack(pady=12)

        btnf = tk.Frame(self, bg=bgroot)
        btnf.pack(pady=12)
        self.confirm_btn = tk.Button(btnf, text="Confirm", command=self.do_confirm,
                                     bg=accent, fg="white", font=fontbtn, width=12, pady=5)
        self.confirm_btn.pack(side="left", padx=8)
        tk.Button(btnf, text="Cancel", command=self.destroy, bg=bgactive, fg=text, font=fontbtn, width=10, pady=5).pack(side="left", padx=8)

    def _style_entry(self, e):
        e.configure(bg=bgcard, fg=text, insertbackground=text,
                    relief="flat", highlightthickness=2, highlightbackground=border,
                    highlightcolor=accent, font=fontbody, bd=0)
        def fin(ev): e.config(highlightcolor=accent, highlightbackground=accent)
        def fout(ev): e.config(highlightcolor=border, highlightbackground=border)
        e.bind("<FocusIn>", fin)
        e.bind("<FocusOut>", fout)

    def set_amount(self, amt):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, str(amt))
        self.msg.config(text="")

    def do_confirm(self):
        try:
            amt = float(self.entry.get())
            if amt <= 0: raise ValueError
        except:
            self.msg.config(text="❌ Enter valid amount > 0")
            return
        ok, msg = self.storage.top_up(self.username, amt)
        if ok:
            self.msg.config(text="✅ " + msg, fg=success)
            self.on_success()
            self.after(1500, self.destroy)
        else:
            self.msg.config(text="❌ " + msg)