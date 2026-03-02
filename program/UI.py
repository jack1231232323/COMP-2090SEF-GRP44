# ui_helpers.py
import tkinter as tk
from config import *

# Animation functions
def fade_in(widget, duration=300):
    """Fade in animation for widgets"""
    try:
        if not widget.winfo_exists():
            return
        widget.attributes('-alpha', 0.0)
        
        def update_alpha(alpha=0.0):
            try:
                if widget.winfo_exists():
                    alpha += 0.1
                    widget.attributes('-alpha', min(alpha, 1.0))
                    if alpha < 1.0:
                        widget.after(30, lambda: update_alpha(alpha))
            except:
                pass
        widget.after(50, lambda: update_alpha())
    except:
        pass

def fade_out(widget, on_complete=None):
    """Fade out animation for widgets"""
    try:
        if not widget.winfo_exists():
            if on_complete:
                on_complete()
            return
        
        def update_alpha(alpha=1.0):
            try:
                if widget.winfo_exists():
                    alpha -= 0.1
                    if alpha > 0:
                        widget.attributes('-alpha', alpha)
                        widget.after(30, lambda: update_alpha(alpha))
                    else:
                        if on_complete:
                            on_complete()
            except:
                if on_complete:
                    on_complete()
        update_alpha()
    except:
        if on_complete:
            on_complete()

def pulse_button(button):
    """Pulse animation for buttons"""
    try:
        if not button.winfo_exists():
            return
        original_bg = button.cget('bg')
        
        def pulse(count=0):
            try:
                if button.winfo_exists() and count < 6:
                    if count % 2 == 0:
                        # Darken the button
                        r, g, b = button.winfo_rgb(original_bg)
                        darker = f'#{int(r/256*0.8):02x}{int(g/256*0.8):02x}{int(b/256*0.8):02x}'
                        button.config(bg=darker)
                    else:
                        button.config(bg=original_bg)
                    button.after(100, lambda: pulse(count + 1))
                else:
                    button.config(bg=original_bg)
            except:
                button.config(bg=original_bg)
        pulse()
    except:
        pass

def shake_widget(widget):
    """Shake animation for errors"""
    try:
        if not widget.winfo_exists():
            return
        original_x = widget.winfo_x()
        
        def shake(count=0):
            try:
                if widget.winfo_exists() and count < 6:
                    offset = 5 if count % 2 == 0 else -5
                    widget.place(x=original_x + offset)
                    widget.after(50, lambda: shake(count + 1))
                else:
                    widget.place(x=original_x)
            except:
                widget.place(x=original_x)
        shake()
    except:
        pass

def slide_down(widget):
    """Slide down animation"""
    try:
        if not widget.winfo_exists():
            return
        widget.pack_forget()
        widget.pack(fill="x", pady=5)
    except:
        pass

def bounce_effect(widget):
    """Bounce effect for buttons"""
    try:
        if not widget.winfo_exists():
            return
        original_y = widget.winfo_y()
        
        def bounce(count=0):
            try:
                if widget.winfo_exists() and count < 4:
                    offset = -3 if count % 2 == 0 else 0
                    widget.place(y=original_y + offset)
                    widget.after(50, lambda: bounce(count + 1))
                else:
                    widget.place(y=original_y)
            except:
                widget.place(y=original_y)
        bounce()
    except:
        pass

def style_entry(widget: tk.Entry):
    widget.configure(
        bg=BG_CARD, fg=TEXT, insertbackground=TEXT,
        relief="flat", highlightthickness=2, highlightbackground=BORDER,
        highlightcolor=ACCENT, font=FONT_BODY, bd=0
    )
    
    # Add focus animation
    def on_focus_in(e):
        widget.config(highlightcolor=ACCENT, highlightbackground=ACCENT)
    
    def on_focus_out(e):
        widget.config(highlightcolor=BORDER, highlightbackground=BORDER)
    
    widget.bind("<FocusIn>", on_focus_in)
    widget.bind("<FocusOut>", on_focus_out)

def create_button(parent, text, command, bg=ACCENT, fg="white",
                  width=14, pady=8, **kwargs):
    btn = tk.Button(
        parent, text=text, command=lambda: [command(), pulse_button(btn)],
        bg=bg, fg=fg,
        activebackground=ACCENT_H if bg == ACCENT else BG_HOVER,
        relief="flat", bd=0, highlightthickness=0,
        font=FONT_BTN, width=width, pady=pady, cursor="hand2",
        **kwargs
    )

    def on_enter(e): 
        btn.config(bg=ACCENT_H if bg == ACCENT else BG_HOVER)
        # Slight scale effect
        btn.config(font=(FONT_BTN[0], FONT_BTN[1]+1, "bold"))
    
    def on_leave(e): 
        btn.config(bg=bg)
        btn.config(font=FONT_BTN)
    
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    return btn

def create_modern_card(parent, **kwargs):
    """Create a modern card with hover effect"""
    card = tk.Frame(parent, bg=BG_CARD, highlightthickness=1,
                   highlightbackground=BORDER, **kwargs)
    
    # Add hover effect
    def on_enter(e):
        card.config(highlightbackground=ACCENT, highlightthickness=2)
    
    def on_leave(e):
        card.config(highlightbackground=BORDER, highlightthickness=1)
    
    card.bind("<Enter>", on_enter)
    card.bind("<Leave>", on_leave)
    
    return card