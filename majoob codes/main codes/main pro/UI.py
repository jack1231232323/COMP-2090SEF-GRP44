# UI.py
# Jack's part - animations and styling helpers
# Choi's part - button creation and entry styling
# Guo's part - pulse and shake effects

import tkinter as tk
from config import *

# Jack's fade effects
def fade_in(w, duration=300):
    try:
        if not w.winfo_exists():
            return
        w.attributes('-alpha', 0.0)
        alpha = 0.0
        def step():
            nonlocal alpha
            try:
                if w.winfo_exists():
                    alpha += 0.1
                    w.attributes('-alpha', min(alpha, 1.0))
                    if alpha < 1.0:
                        w.after(30, step)
            except:
                pass
        w.after(50, step)
    except:
        pass

def fade_out(w, callback=None):
    try:
        if not w.winfo_exists():
            if callback: callback()
            return
        alpha = 1.0
        def step():
            nonlocal alpha
            try:
                if w.winfo_exists():
                    alpha -= 0.1
                    if alpha > 0:
                        w.attributes('-alpha', alpha)
                        w.after(30, step)
                    else:
                        if callback: callback()
                else:
                    if callback: callback()
            except:
                if callback: callback()
        step()
    except:
        if callback: callback()

# Guo's pulse_button
def pulse_button(btn):
    try:
        if not btn.winfo_exists():
            return
        orig = btn.cget('bg')
        def pulse(count=0):
            if btn.winfo_exists() and count < 6:
                if count % 2 == 0:
                    r,g,b = btn.winfo_rgb(orig)
                    darker = f'#{int(r/256*0.7):02x}{int(g/256*0.7):02x}{int(b/256*0.7):02x}'
                    btn.config(bg=darker)
                else:
                    btn.config(bg=orig)
                btn.after(100, lambda: pulse(count+1))
            else:
                btn.config(bg=orig)
        pulse()
    except:
        pass

# Guo's shake_widget
def shake_widget(w):
    try:
        if not w.winfo_exists():
            return
        ox = w.winfo_x()
        def shake(count=0):
            if w.winfo_exists() and count < 6:
                off = 5 if count%2==0 else -5
                w.place(x=ox+off)
                w.after(50, lambda: shake(count+1))
            else:
                w.place(x=ox)
        shake()
    except:
        pass

# Choi's style_entry
def style_entry(entry):
    entry.configure(
        bg=BG_CARD, fg=TEXT, insertbackground=TEXT,
        relief="flat", highlightthickness=2, highlightbackground=BORDER,
        highlightcolor=ACCENT, font=FONT_BODY, bd=0
    )
    def on_focus_in(e):
        entry.config(highlightcolor=ACCENT, highlightbackground=ACCENT)
    def on_focus_out(e):
        entry.config(highlightcolor=BORDER, highlightbackground=BORDER)
    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# Choi's create_button
def create_button(parent, text, cmd, bg=ACCENT, fg="white",
                  width=14, pady=8, **kw):
    btn = tk.Button(
        parent, text=text, command=lambda: [cmd(), pulse_button(btn)],
        bg=bg, fg=fg,
        activebackground=ACCENT_H if bg==ACCENT else BG_HOVER,
        relief="flat", bd=0, highlightthickness=0,
        font=FONT_BTN, width=width, pady=pady, cursor="hand2",
        **kw
    )
    def on_enter(e):
        btn.config(bg=ACCENT_H if bg==ACCENT else BG_HOVER)
        btn.config(font=(FONT_BTN[0], FONT_BTN[1]+1, "bold"))
    def on_leave(e):
        btn.config(bg=bg)
        btn.config(font=FONT_BTN)
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn