import tkinter as tk
from config import *

def fade_in(w, d=300):
    try:
        if not w.winfo_exists():
            return
        w.attributes('-alpha', 0.0)
        
        def upd(a=0.0):
            try:
                if w.winfo_exists():
                    a += 0.1
                    w.attributes('-alpha', min(a, 1.0))
                    if a < 1.0:
                        w.after(30, lambda: upd(a))
            except:
                pass
        w.after(50, lambda: upd())
    except:
        pass

def fade_out(w, on_complete=None):
    try:
        if not w.winfo_exists():
            if on_complete:
                on_complete()
            return
        
        def upd(a=1.0):
            try:
                if w.winfo_exists():
                    a -= 0.1
                    if a > 0:
                        w.attributes('-alpha', a)
                        w.after(30, lambda: upd(a))
                    else:
                        if on_complete:
                            on_complete()
            except:
                if on_complete:
                    on_complete()
        upd()
    except:
        if on_complete:
            on_complete()

def pulse_button(b):
    try:
        if not b.winfo_exists():
            return
        orig = b.cget('bg')
        
        def p(c=0):
            try:
                if b.winfo_exists() and c < 6:
                    if c % 2 == 0:
                        r, g, b_ = b.winfo_rgb(orig)
                        darker = f'#{int(r/256*0.8):02x}{int(g/256*0.8):02x}{int(b_/256*0.8):02x}'
                        b.config(bg=darker)
                    else:
                        b.config(bg=orig)
                    b.after(100, lambda: p(c + 1))
                else:
                    b.config(bg=orig)
            except:
                b.config(bg=orig)
        p()
    except:
        pass

def shake_widget(w):
    try:
        if not w.winfo_exists():
            return
        ox = w.winfo_x()
        
        def s(c=0):
            try:
                if w.winfo_exists() and c < 6:
                    off = 5 if c % 2 == 0 else -5
                    w.place(x=ox + off)
                    w.after(50, lambda: s(c + 1))
                else:
                    w.place(x=ox)
            except:
                w.place(x=ox)
        s()
    except:
        pass

def slide_down(w):
    try:
        if not w.winfo_exists():
            return
        w.pack_forget()
        w.pack(fill="x", pady=5)
    except:
        pass

def bounce_effect(w):
    try:
        if not w.winfo_exists():
            return
        oy = w.winfo_y()
        
        def b(c=0):
            try:
                if w.winfo_exists() and c < 4:
                    off = -3 if c % 2 == 0 else 0
                    w.place(y=oy + off)
                    w.after(50, lambda: b(c + 1))
                else:
                    w.place(y=oy)
            except:
                w.place(y=oy)
        b()
    except:
        pass

def style_entry(w):
    w.configure(
        bg=BG_CARD, fg=TEXT, insertbackground=TEXT,
        relief="flat", highlightthickness=2, highlightbackground=BORDER,
        highlightcolor=ACCENT, font=FONT_BODY, bd=0
    )
    
    def on_focus_in(e):
        w.config(highlightcolor=ACCENT, highlightbackground=ACCENT)
    
    def on_focus_out(e):
        w.config(highlightcolor=BORDER, highlightbackground=BORDER)
    
    w.bind("<FocusIn>", on_focus_in)
    w.bind("<FocusOut>", on_focus_out)

def create_button(p, txt, cmd, bg=ACCENT, fg="white",
                  width=14, pady=8, **kw):
    b = tk.Button(
        p, text=txt, command=lambda: [cmd(), pulse_button(b)],
        bg=bg, fg=fg,
        activebackground=ACCENT_H if bg == ACCENT else BG_HOVER,
        relief="flat", bd=0, highlightthickness=0,
        font=FONT_BTN, width=width, pady=pady, cursor="hand2",
        **kw
    )

    def on_enter(e): 
        b.config(bg=ACCENT_H if bg == ACCENT else BG_HOVER)
        b.config(font=(FONT_BTN[0], FONT_BTN[1]+1, "bold"))
    
    def on_leave(e): 
        b.config(bg=bg)
        b.config(font=FONT_BTN)
    
    b.bind("<Enter>", on_enter)
    b.bind("<Leave>", on_leave)
    return b

def create_modern_card(p, **kw):
    c = tk.Frame(p, bg=BG_CARD, highlightthickness=1,
                highlightbackground=BORDER, **kw)
    
    def on_enter(e):
        c.config(highlightbackground=ACCENT, highlightthickness=2)
    
    def on_leave(e):
        c.config(highlightbackground=BORDER, highlightthickness=1)
    
    c.bind("<Enter>", on_enter)
    c.bind("<Leave>", on_leave)
    
    return c