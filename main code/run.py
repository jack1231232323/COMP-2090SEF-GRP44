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
        self._center()

        self.storage = Storage()
        self.current_user = None

        self._show_auth()

    def _center(self):
        self.update_idletasks()
        w = self.winfo_width()
        h = self.winfo_height()
        x = (self.winfo_screenwidth() - w) // 2
        y = (self.winfo_screenheight() - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _show_auth(self):
        AuthWindow(self, self.storage, self._on_login)

    def _on_login(self, username):
        self.current_user = username
        
        if username == "admin":
            for widget in self.winfo_children():
                widget.destroy()
            AdminWindow(self, self.storage)
        else:
            for widget in self.winfo_children():
                widget.destroy()
            Dashboard(self, self.storage, username, self._logout)

    def _logout(self):
        self.current_user = None
        for widget in self.winfo_children():
            widget.destroy()
        self._show_auth()

if __name__ == "__main__":
    app = MahjongApp()
    app.mainloop()