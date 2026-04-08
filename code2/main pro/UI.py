import tkinter as tk
from config import *

# just some helper functions for styling

def style_entry(e):
    e.configure(bg=BG_CARD, fg=TEXT, insertbackground=TEXT,
                relief="flat", highlightthickness=2, highlightbackground=BORDER,
                highlightcolor=ACCENT, font=FONT_BODY, bd=0)
    def fin(e): e.config(highlightcolor=ACCENT, highlightbackground=ACCENT)
    def fout(e): e.config(highlightcolor=BORDER, highlightbackground=BORDER)
    e.bind("<FocusIn>", fin)
    e.bind("<FocusOut>", fout)

def mk_btn(parent, txt, cmd, bg=ACCENT, fg="white", width=14, pady=8, **kw):
    btn = tk.Button(parent, text=txt, command=cmd,
                    bg=bg, fg=fg, activebackground=ACCENT_H if bg==ACCENT else BG_HOVER,
                    relief="flat", bd=0, highlightthickness=0,
                    font=FONT_BTN, width=width, pady=pady, cursor="hand2", **kw)
    def enter(e): 
        btn.config(bg=ACCENT_H if bg==ACCENT else BG_HOVER)
        btn.config(font=(FONT_BTN[0], FONT_BTN[1]+1, "bold"))
    def leave(e): 
        btn.config(bg=bg)
        btn.config(font=FONT_BTN)
    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn