import tkinter as tk
from tkinter import ttk, messagebox
from config import *
from UI import create_button, style_entry, fade_in, pulse_button
from datetime import datetime
import hashlib
import os
import json
import shutil

class AdminWindow(tk.Toplevel):
    def __init__(self, master, storage):
        super().__init__(master)
        self.master = master
        self.storage = storage
        
        self.title("Admin Dashboard - System Management")
        self.configure(bg=BG_ROOT)
        self.geometry("1100x700")
        self.resizable(True, True)
        
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1100) // 2
        y = (self.winfo_screenheight() - 700) // 2  # typo here - missing self.
        self.geometry(f"1100x700+{x}+{y}")
        
        self.transient(master)
        self.grab_set()
        
        self.do_ui()
        self.protocol("WM_DELETE_WINDOW", self.do_close)
        
        self.after(100, lambda: fade_in(self))
        
    def do_close(self):
        self.destroy()
        
    def do_ui(self):
        main = tk.Frame(self, bg=BG_ROOT)
        main.pack(fill="both", expand=True)
        
        header = tk.Frame(main, bg=BG_CARD, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        tframe = tk.Frame(header, bg=BG_CARD)
        tframe.pack(side="left", padx=20, pady=15)
        
        tk.Label(tframe, text="👑 ADMIN DASHBOARD", font=FONT_TITLE,
                fg=ACCENT, bg=BG_CARD).pack(side="left")
        
        aframe = tk.Frame(header, bg=BG_CARD)
        aframe.pack(side="right", padx=20, pady=10)
        
        tk.Button(aframe, text="🔄 Refresh All", command=self.do_refresh,
                 bg=ACCENT, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(aframe, text="💾 Backup Now", command=self.do_backup,
                 bg=SUCCESS, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(aframe, text="📊 Statistics", command=self.do_stats,
                 bg=WARNING, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        nb = ttk.Notebook(main)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        
        style = ttk.Style()
        style.configure("TNotebook", background=BG_ROOT)
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 10, "bold"))
        
        self.tab1(nb)
        self.tab2(nb)
        self.tab3(nb)
        self.tab4(nb)
        
    def tab1(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="👥 USER MANAGEMENT")
        
        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0, 10))
        ctrl.pack_propagate(False)
        
        tk.Label(ctrl, text="User Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        bf = tk.Frame(ctrl, bg=BG_CARD)
        bf.pack(side="right", padx=20)
        
        tk.Button(bf, text="➕ ADD NEW USER", command=self.add_user,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(bf, text="🗑️ DELETE SELECTED", command=self.del_sel_user,
                 bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(bf, text="✏️ EDIT SELECTED", command=self.edit_sel_user,
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        cols = ("Username", "Balance", "Password Hash", "Actions")
        self.utree = ttk.Treeview(tab, columns=cols, show="headings", height=15)
        
        self.utree.heading("Username", text="USERNAME")
        self.utree.heading("Balance", text="BALANCE ($)")
        self.utree.heading("Password Hash", text="PASSWORD HASH (SHA-256)")
        self.utree.heading("Actions", text="QUICK ACTIONS")
        
        self.utree.column("Username", width=150, anchor="center")
        self.utree.column("Balance", width=100, anchor="center")
        self.utree.column("Password Hash", width=400, anchor="w")
        self.utree.column("Actions", width=200, anchor="center")
        
        sb = ttk.Scrollbar(tab, orient="vertical", command=self.utree.yview)
        self.utree.configure(yscrollcommand=sb.set)
        
        self.utree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.utree.bind("<Double-1>", self.do_edit)
        
        self.load_users()
        
    def tab2(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="🎲 TABLE MANAGEMENT")
        
        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0, 10))
        ctrl.pack_propagate(False)
        
        tk.Label(ctrl, text="Table Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        tk.Label(ctrl, text="Click on any table to manage", font=FONT_SMALL,
                fg=TEXT_DIM, bg=BG_CARD).pack(side="right", padx=20)
        
        can = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        sb = tk.Scrollbar(tab, orient="vertical", command=can.yview)
        sf = tk.Frame(can, bg=BG_ROOT)
        
        sf.bind(
            "<Configure>",
            lambda e: can.configure(scrollregion=can.bbox("all"))
        )
        
        can.create_window((0, 0), window=sf, anchor="nw")
        can.configure(yscrollcommand=sb.set)
        
        can.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        cf = tk.Frame(sf, bg=BG_ROOT)
        cf.pack(fill="both", expand=True)
        
        self.cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = self.make_card(cf, tid)
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cf.grid_columnconfigure(col, weight=1)
            cf.grid_rowconfigure(row, weight=1)
            
    def make_card(self, parent, tid):
        card = tk.Frame(parent, bg=BG_CARD, relief="raised", bd=2)
        
        hdr = tk.Frame(card, bg=BG_CARD)
        hdr.pack(fill="x", padx=15, pady=10)
        
        tk.Label(hdr, text=f"TABLE {tid}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left")
        
        b = self.storage.bookings.get(tid)
        if b:
            st = "🔴 IN USE"
            sc = ERROR
        else:
            st = "🟢 AVAILABLE"
            sc = SUCCESS
        
        lbl = tk.Label(hdr, text=st, font=("Segoe UI", 10, "bold"),
                      fg=sc, bg=BG_CARD)
        lbl.pack(side="right")
        
        tk.Frame(card, bg=BORDER, height=2).pack(fill="x", padx=10)
        
        det = tk.Frame(card, bg=BG_CARD)
        det.pack(fill="x", padx=15, pady=10)
        
        if b:
            inf = [
                f"👤 User: {b.username}",
                f"⏱️ Hours: {b.hours}",
                f"💰 Cost: ${b.cost}",
                f"🕒 Started: {b.start_time[:16]}"
            ]
            for l in inf:
                tk.Label(det, text=l, font=("Segoe UI", 10),
                        fg=TEXT, bg=BG_CARD, anchor="w").pack(fill="x", pady=1)
        else:
            tk.Label(det, text="No active booking", font=("Segoe UI", 12),
                    fg=TEXT_DIM, bg=BG_CARD).pack(pady=20)
        
        acts = tk.Frame(card, bg=BG_CARD)
        acts.pack(fill="x", padx=15, pady=10)
        
        if b:
            tk.Button(acts, text="🔴 FORCE CLOSE", 
                     command=lambda t=tid: self.force_close(t),
                     bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                     padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=2, fill="x", expand=True)
        
        tk.Button(acts, text="🔄 RESET TABLE", 
                 command=lambda t=tid: self.reset_tbl(t),
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="right" if b else "left", padx=2, fill="x", expand=True)
        
        return card
        
    def tab3(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="📋 BOOKING MANAGEMENT")
        
        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0, 10))
        ctrl.pack_propagate(False)
        
        tk.Label(ctrl, text="Booking Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        bf = tk.Frame(ctrl, bg=BG_CARD)
        bf.pack(side="right", padx=20)
        
        tk.Button(bf, text="🗑️ CLEAR ALL BOOKINGS", command=self.clear_all_bookings,
                 bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(bf, text="📊 VIEW STATISTICS", command=self.show_booking_stats,
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        cols = ("Table", "User", "Hours", "Cost", "Start Time", "End Time", "Actions")
        self.btree = ttk.Treeview(tab, columns=cols, show="headings", height=15)
        
        self.btree.heading("Table", text="TABLE")
        self.btree.heading("User", text="USER")
        self.btree.heading("Hours", text="HOURS")
        self.btree.heading("Cost", text="COST ($)")
        self.btree.heading("Start Time", text="START TIME")
        self.btree.heading("End Time", text="END TIME")
        self.btree.heading("Actions", text="ACTIONS")
        
        self.btree.column("Table", width=80, anchor="center")
        self.btree.column("User", width=120, anchor="center")
        self.btree.column("Hours", width=60, anchor="center")
        self.btree.column("Cost", width=80, anchor="center")
        self.btree.column("Start Time", width=150, anchor="center")
        self.btree.column("End Time", width=150, anchor="center")
        self.btree.column("Actions", width=100, anchor="center")
        
        sb = ttk.Scrollbar(tab, orient="vertical", command=self.btree.yview)
        self.btree.configure(yscrollcommand=sb.set)
        
        self.btree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        sb.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        self.btree.bind("<ButtonRelease-1>", self.on_click_booking)
        
        self.load_bookings()
        
    def tab4(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="⚙️ SYSTEM SETTINGS")
        
        can = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        sb = tk.Scrollbar(tab, orient="vertical", command=can.yview)
        sf = tk.Frame(can, bg=BG_ROOT)
        
        sf.bind(
            "<Configure>",
            lambda e: can.configure(scrollregion=can.bbox("all"))
        )
        
        can.create_window((0, 0), window=sf, anchor="nw")
        can.configure(yscrollcommand=sb.set)
        
        can.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")
        
        sets = tk.Frame(sf, bg=BG_CARD, padx=30, pady=30)
        sets.pack(fill="both", expand=True, padx=20, pady=20)
        
        tk.Label(sets, text="⚙️ SYSTEM SETTINGS", font=("Segoe UI", 20, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 30))
        
        self.mk_section(sets, "💰 RATE SETTINGS", 0)
        
        rf = tk.Frame(sets, bg=BG_CARD)
        rf.pack(fill="x", pady=10)
        
        tk.Label(rf, text="Hourly Rate ($):", font=("Segoe UI", 12),
                fg=TEXT, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        
        self.rv = tk.StringVar(value=str(RATE_PER_HOUR))
        re = tk.Entry(rf, textvariable=self.rv, 
                     font=("Segoe UI", 12), width=10, justify="center")
        re.pack(side="left", padx=10)
        
        tk.Button(rf, text="UPDATE RATE", command=self.upd_rate,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=10)
        
        self.mk_section(sets, "💾 DATA MANAGEMENT", 1)
        
        df = tk.Frame(sets, bg=BG_CARD)
        df.pack(fill="x", pady=15)
        
        r1 = tk.Frame(df, bg=BG_CARD)
        r1.pack(fill="x", pady=5)
        
        tk.Button(r1, text="💾 BACKUP DATA", command=self.do_backup,
                 bg=ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        tk.Button(r1, text="📂 RESTORE DATA", command=self.do_restore,
                 bg=ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        r2 = tk.Frame(df, bg=BG_CARD)
        r2.pack(fill="x", pady=5)
        
        tk.Button(r2, text="🗑️ RESET ALL DATA", command=self.do_reset_all,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        tk.Button(r2, text="📊 VIEW STATISTICS", command=self.do_stats,
                 bg=WARNING, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        self.mk_section(sets, "📊 SYSTEM STATISTICS", 2)
        
        sf2 = tk.Frame(sets, bg=BG_CARD, relief="solid", bd=1)
        sf2.pack(fill="x", pady=10, ipady=10)
        
        self.upd_stats(sf2)
        
    def mk_section(self, parent, title, idx):
        s = tk.Frame(parent, bg=BG_CARD)
        s.pack(fill="x", pady=(20 if idx > 0 else 0, 5))
        
        tk.Label(s, text=title, font=("Segoe UI", 14, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(anchor="w")
        
        tk.Frame(s, bg=BORDER, height=2).pack(fill="x", pady=5)
        
    def upd_stats(self, parent):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        
        g = tk.Frame(parent, bg=BG_CARD)
        g.pack(fill="x", padx=10, pady=5)
        
        r1 = tk.Frame(g, bg=BG_CARD)
        r1.pack(fill="x", pady=5)
        
        tk.Label(r1, text=f"👥 Total Users:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(r1, text=f"{tu}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20)
        
        r2 = tk.Frame(g, bg=BG_CARD)
        r2.pack(fill="x", pady=5)
        
        tk.Label(r2, text=f"📋 Active Bookings:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(r2, text=f"{tb}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20)
        
        r3 = tk.Frame(g, bg=BG_CARD)
        r3.pack(fill="x", pady=5)
        
        tk.Label(r3, text=f"💰 Total Revenue:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(r3, text=f"${tr:.2f}", font=("Segoe UI", 16, "bold"),
                fg=SUCCESS, bg=BG_CARD).pack(side="left", padx=20)
        
    def load_users(self):
        for i in self.utree.get_children():
            self.utree.delete(i)
        
        for u, user in self.storage.users.items():
            af = tk.Frame(self.utree, bg=BG_CARD)
            
            eb = tk.Button(af, text="✏️", font=("Segoe UI", 10),
                          command=lambda x=u: self.edit_user(x),
                          bg=ACCENT, fg="white", width=3, cursor="hand2")
            eb.pack(side="left", padx=2)
            
            db = tk.Button(af, text="🗑️", font=("Segoe UI", 10),
                          command=lambda x=u: self.del_user(x),
                          bg=ERROR, fg="white", width=3, cursor="hand2")
            db.pack(side="left", padx=2)
            
            self.utree.insert("", "end", values=(
                u,
                f"${user.balance:.2f}",
                user.password_hash[:20] + "...",
                "Click to manage"
            ), tags=(u,))
            
    def load_bookings(self):
        for i in self.btree.get_children():
            self.btree.delete(i)
        
        for tid, b in self.storage.bookings.items():
            et = b.end_time_str if hasattr(b, 'end_time_str') else "N/A"
            self.btree.insert("", "end", values=(
                tid,
                b.username,
                b.hours,
                f"${b.cost:.2f}",
                b.start_time[:16],
                et,
                "❌ CLOSE"
            ), tags=(tid,))
            
    def do_refresh(self):
        self.load_users()
        self.load_bookings()
        messagebox.showinfo("Success", "✨ All data refreshed successfully!")
        
    def del_sel_user(self):
        s = self.utree.selection()
        if not s:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        item = self.utree.item(s[0])
        u = item['values'][0]
        self.del_user(u)
        
    def edit_sel_user(self):
        s = self.utree.selection()
        if not s:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        item = self.utree.item(s[0])
        u = item['values'][0]
        self.edit_user(u)
        
    def del_user(self, u):
        if u == "admin":
            messagebox.showerror("Error", "❌ Cannot delete admin user!")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Delete user '{u}'?"):
            ub = [b for b in self.storage.bookings.values() if b.username == u]
            if ub:
                for tid, b in list(self.storage.bookings.items()):
                    if b.username == u:
                        del self.storage.bookings[tid]
            
            del self.storage.users[u]
            self.storage.save()
            self.load_users()
            self.load_bookings()
            messagebox.showinfo("Success", f"✅ User '{u}' deleted!")
            
    def edit_user(self, u):
        user = self.storage.get_user(u)
        if user:
            self.edit_dialog(u, user.balance)
            
    def edit_dialog(self, u, bal):
        d = tk.Toplevel(self)
        d.title(f"Edit User: {u}")
        d.configure(bg=BG_ROOT)
        d.geometry("400x350")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400) // 2
        y = (d.winfo_screenheight() - 350) // 2
        d.geometry(f"400x350+{x}+{y}")
        
        f = tk.Frame(d, bg=BG_CARD, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        
        tk.Label(f, text=f"EDIT USER: {u}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 20))
        
        tk.Label(f, text="New Balance ($):", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        be = tk.Entry(f, font=("Segoe UI", 12))
        be.insert(0, str(bal))
        be.pack(fill="x", pady=(0, 15))
        
        tk.Label(f, text="New Password (leave blank to keep):", font=("Segoe UI", 10),
                fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        pe = tk.Entry(f, font=("Segoe UI", 12), show="•")
        pe.pack(fill="x", pady=(0, 20))
        
        bf = tk.Frame(f, bg=BG_CARD)
        bf.pack(fill="x", pady=10)
        
        def upd():
            try:
                nb = float(be.get())
                user = self.storage.get_user(u)
                user.balance = nb
                
                np = pe.get()
                if np:
                    if len(np) < 4:
                        messagebox.showerror("Error", "Password too short!")
                        return
                    user.password_hash = hashlib.sha256(np.encode()).hexdigest()
                
                self.storage.save()
                self.load_users()
                messagebox.showinfo("Success", "✅ User updated!")
                d.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid balance!")
        
        tk.Button(bf, text="💾 SAVE CHANGES", command=upd,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        
        tk.Button(bf, text="✕ CANCEL", command=d.destroy,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)
        
    def do_edit(self, e):
        self.edit_sel_user()
        
    def on_click_booking(self, e):
        s = self.btree.selection()
        if s:
            item = self.btree.item(s[0])
            tid = item['values'][0]
            if messagebox.askyesno("Close Booking", f"Close table {tid}?"):
                self.force_close(tid)
        
    def do_stats(self):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        
        s = f"""📊 SYSTEM STATISTICS

👥 Total Users: {tu}
📋 Active Bookings: {tb}
💰 Total Revenue: ${tr:.2f}

🟢 Available Tables: {4 - tb}
🔴 Occupied Tables: {tb}"""
        
        messagebox.showinfo("Statistics", s)
        
    def show_booking_stats(self):
        self.do_stats()
        
    def force_close(self, tid):
        if messagebox.askyesno("Confirm", f"Force close Table {tid}?"):
            if tid in self.storage.bookings:
                del self.storage.bookings[tid]
                self.storage.save()
                self.do_refresh()
                messagebox.showinfo("Success", f"✅ Table {tid} closed")
                
    def reset_tbl(self, tid):
        if tid in self.storage.bookings:
            if messagebox.askyesno("Confirm", f"Reset Table {tid}?"):
                del self.storage.bookings[tid]
                self.storage.save()
                self.do_refresh()
                messagebox.showinfo("Success", f"✅ Table {tid} reset")
        else:
            messagebox.showinfo("Info", f"Table {tid} is already empty")
            
    def clear_all_bookings(self):
        if messagebox.askyesno("⚠️ WARNING", "Clear ALL bookings? This cannot be undone!"):
            self.storage.bookings.clear()
            self.storage.save()
            self.do_refresh()
            messagebox.showinfo("Success", "✅ All bookings cleared")
            
    def upd_rate(self):
        try:
            nr = int(self.rv.get())
            if nr <= 0:
                raise ValueError
                
            global RATE_PER_HOUR
            RATE_PER_HOUR = nr
            messagebox.showinfo("Success", f"✅ Rate updated to ${nr}/hour")
        except:
            messagebox.showerror("Error", "Please enter a valid positive number")
            
    def do_backup(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bf = f"mahjong_backup_{ts}.json"
        
        try:
            shutil.copy2(DATA_FILE, bf)
            messagebox.showinfo("Success", f"✅ Data backed up to {bf}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")
            
    def do_restore(self):
        from tkinter import filedialog
        
        fn = filedialog.askopenfilename(
            title="Select backup file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if fn:
            try:
                with open(fn, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
                self.storage._load()
                self.do_refresh()
                messagebox.showinfo("Success", "✅ Data restored successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Restore failed: {e}")
                
    def do_reset_all(self):
        if messagebox.askyesno("⚠️ WARNING", "This will DELETE ALL DATA! Are you sure?"):
            if messagebox.askyesno("⚠️ FINAL WARNING", "This cannot be undone. Continue?"):
                self.storage.users.clear()
                self.storage.bookings.clear()
                self.storage._create_test_data()
                self.do_refresh()
                messagebox.showinfo("Success", "✅ All data has been reset")
                
    def add_user(self):
        d = tk.Toplevel(self)
        d.title("Add New User")
        d.configure(bg=BG_ROOT)
        d.geometry("400x400")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400) // 2
        y = (d.winfo_screenheight() - 400) // 2
        d.geometry(f"400x400+{x}+{y}")
        
        f = tk.Frame(d, bg=BG_CARD, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        
        tk.Label(f, text="➕ ADD NEW USER", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 20))
        
        tk.Label(f, text="Username:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        ue = tk.Entry(f, font=("Segoe UI", 12))
        ue.pack(fill="x", pady=(0, 15))
        
        tk.Label(f, text="Password:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        pe = tk.Entry(f, font=("Segoe UI", 12), show="•")
        pe.pack(fill="x", pady=(0, 15))
        
        tk.Label(f, text="Initial Balance ($):", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        be = tk.Entry(f, font=("Segoe UI", 12))
        be.insert(0, "0")
        be.pack(fill="x", pady=(0, 20))
        
        def do_add():
            u = ue.get().strip()
            p = pe.get()
            
            try:
                b = float(be.get())
            except:
                messagebox.showerror("Error", "Invalid balance amount")
                return
                
            if not u or not p:
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            ok, msg = self.storage.register(u, p)
            if ok:
                user = self.storage.get_user(u)
                if user:
                    user.balance = b
                    self.storage.save()
                    
                self.load_users()
                messagebox.showinfo("Success", f"✅ User {u} created!")
                d.destroy()
            else:
                messagebox.showerror("Error", msg)
                
        bf = tk.Frame(f, bg=BG_CARD)
        bf.pack(fill="x", pady=10)
        
        tk.Button(bf, text="✅ CREATE USER", command=do_add,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        
        tk.Button(bf, text="✕ CANCEL", command=d.destroy,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)