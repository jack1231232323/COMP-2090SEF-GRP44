import tkinter as tk
from config import *

# ----- animations -----
def fade_in(w, dur=300):
    try:
        if not w.winfo_exists(): return
        w.attributes('-alpha', 0.0)
        a = 0.0
        def step():
            nonlocal a
            try:
                if w.winfo_exists():
                    a += 0.1
                    w.attributes('-alpha', min(a,1.0))
                    if a < 1.0:
                        w.after(30, step)
            except: pass
        w.after(50, step)
    except: pass

def fade_out(w, cb=None):
    try:
        if not w.winfo_exists():
            if cb: cb()
            return
        a = 1.0
        def step():
            nonlocal a
            try:
                if w.winfo_exists():
                    a -= 0.1
                    if a > 0:
                        w.attributes('-alpha', a)
                        w.after(30, step)
                    else:
                        if cb: cb()
                else:
                    if cb: cb()
            except:
                if cb: cb()
        step()
    except:
        if cb: cb()

def pulse_btn(btn):
    try:
        if not btn.winfo_exists(): return
        orig = btn.cget('bg')
        def _pulse(cnt=0):
            if btn.winfo_exists() and cnt < 6:
                if cnt%2==0:
                    r,g,b = btn.winfo_rgb(orig)
                    darker = f'#{int(r/256*0.7):02x}{int(g/256*0.7):02x}{int(b/256*0.7):02x}'
                    btn.config(bg=darker)
                else:
                    btn.config(bg=orig)
                btn.after(100, lambda: _pulse(cnt+1))
            else:
                btn.config(bg=orig)
        _pulse()
    except: pass

def shake(w):
    try:
        if not w.winfo_exists(): return
        ox = w.winfo_x()
        def _shake(cnt=0):
            if w.winfo_exists() and cnt < 6:
                off = 5 if cnt%2==0 else -5
                w.place(x=ox+off)
                w.after(50, lambda: _shake(cnt+1))
            else:
                w.place(x=ox)
        _shake()
    except: pass

# ----- style helpers -----
def style_entry(e):
    e.configure(bg=BG_CARD, fg=TEXT, insertbackground=TEXT,
                relief="flat", highlightthickness=2, highlightbackground=BORDER,
                highlightcolor=ACCENT, font=FONT_BODY, bd=0)
    def fin(e): e.config(highlightcolor=ACCENT, highlightbackground=ACCENT)
    def fout(e): e.config(highlightcolor=BORDER, highlightbackground=BORDER)
    e.bind("<FocusIn>", fin)
    e.bind("<FocusOut>", fout)

def mk_btn(parent, txt, cmd, bg=ACCENT, fg="white", width=14, pady=8, **kw):
    btn = tk.Button(parent, text=txt, command=lambda: [cmd(), pulse_btn(btn)],
                    bg=bg, fg=fg, activebackground=ACCENT_H if bg==ACCENT else BG_HOVER,
                    relief="flat", bd=0, highlightthickness=0,
                    font=FONT_BTN, width=width, pady=pady, cursor="hand2", **kw)
    def enter(e): btn.config(bg=ACCENT_H if bg==ACCENT else BG_HOVER); btn.config(font=(FONT_BTN[0], FONT_BTN[1]+1, "bold"))
    def leave(e): btn.config(bg=bg); btn.config(font=FONT_BTN)
    btn.bind("<Enter>", enter)
    btn.bind("<Leave>", leave)
    return btn