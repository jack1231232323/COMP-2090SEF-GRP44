# run.py
# Jack's part - main application class and window management
# Choi's part - login routing and dashboard/admin switching
# Guo's part - logout and auth window display

import tkinter as tk
from storage import Storage
from verify import AuthWindow
from dashboard import Dashboard
from admin import AdminWindow
from config import *

class MahjongApp(tk.Tk):
    def __init__(self):  # Jack
        super().__init__()
        self.title("Mahjong Table Management")
        self.configure(bg=BG_ROOT)
        self.geometry("1080x680")
        self.resizable(False, False)
        self.center()

        self.storage = Storage()
        self.current_user = None
        self.show_auth()

    def center(self):  # Jack
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def show_auth(self):  # Guo
        AuthWindow(self, self.storage, self.on_login)

    def on_login(self, username):  # Choi
        self.current_user = username
        for child in self.winfo_children():
            child.destroy()
        if username == "admin":
            AdminWindow(self, self.storage)
        else:
            Dashboard(self, self.storage, username, self.logout)

    def logout(self):  # Guo
        self.current_user = None
        for child in self.winfo_children():
            child.destroy()
        self.show_auth()

if __name__ == "__main__":
    app = MahjongApp()
    app.mainloop()