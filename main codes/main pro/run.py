import tkinter as tk
from storage import Storage
from verify import AuthWindow
from dashboard import Dashboard
from admin import AdminWindow
from config import *

class MahjongApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mahjong Table Management")
        self.configure(bg=BG_ROOT)
        self.geometry("1080x680")
        self.resizable(False, False)
        self.center()

        self.storage = Storage()
        self.cur_user = None

        self.show_auth()

    def center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_auth(self):
        AuthWindow(self, self.storage, self.on_login)

    def on_login(self, username):
        self.cur_user = username
        
        if username == "admin":
            for w in self.winfo_children():
                w.destroy()
            AdminWindow(self, self.storage)
        else:
            for w in self.winfo_children():
                w.destroy()
            Dashboard(self, self.storage, username, self.do_logout)

    def do_logout(self):
        self.cur_user = None
        for w in self.winfo_children():
            w.destroy()
        self.show_auth()

if __name__ == "__main__":
    app = MahjongApp()
    app.mainloop()