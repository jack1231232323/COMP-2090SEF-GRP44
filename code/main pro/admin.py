import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import *
from UI import mk_btn, style_entry, fade_in, pulse_btn
from datetime import datetime
import hashlib, json, shutil

class AdminWindow(tk.Toplevel):
    def __init__(self, master, storage):
        super().__init__(master)
        self.master = master
        self.storage = storage

        self.title("Admin Dashboard - System Mgmt")
        self.configure(bg=BG_ROOT)
        self.geometry("1100x700")
        self.resizable(True, True)

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        xp = (sw - 1100)//2
        yp = (sh - 700)//2
        self.geometry(f"1100x700+{xp}+{yp}")

        self.transient(master)
        self.grab_set()

        self._make_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.after(100, lambda: fade_in(self))

    def _on_close(self):
        self.destroy()

    def _make_ui(self):
        main = tk.Frame(self, bg=BG_ROOT)
        main.pack(fill="both", expand=True)

        # header
        head = tk.Frame(main, bg=BG_CARD, height=70)
        head.pack(fill="x")
        head.pack_propagate(False)

        tframe = tk.Frame(head, bg=BG_CARD)
        tframe.pack(side="left", padx=20, pady=15)
        tk.Label(tframe, text="👑 ADMIN PANEL", font=FONT_TITLE, fg=ACCENT, bg=BG_CARD).pack(side="left")

        aframe = tk.Frame(head, bg=BG_CARD)
        aframe.pack(side="right", padx=20, pady=10)
        tk.Button(aframe, text="🔄 Refresh", command=self._refresh_all,
                  bg=ACCENT, fg="white", font=FONT_BTN, padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        tk.Button(aframe, text="💾 Backup", command=self._backup,
                  bg=SUCCESS, fg="white", font=FONT_BTN, padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        tk.Button(aframe, text="📊 Stats", command=self._stats,
                  bg=WARNING, fg="white", font=FONT_BTN, padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)

        # notebook
        nb = ttk.Notebook(main)
        nb.pack(fill="both", expand=True, padx=10, pady=10)
        style = ttk.Style()
        style.configure("TNotebook", background=BG_ROOT)
        style.configure("TNotebook.Tab", padding=[15,8], font=("Segoe UI",10,"bold"))

        self._tab_users(nb)
        self._tab_tables(nb)
        self._tab_bookings(nb)
        self._tab_settings(nb)

    # ---------- user tab ----------
    def _tab_users(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="👥 USERS")

        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="User Management", font=FONT_HEADING, fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)

        bf = tk.Frame(ctrl, bg=BG_CARD)
        bf.pack(side="right", padx=20)
        tk.Button(bf, text="➕ ADD", command=self._add_user, bg=SUCCESS, fg="white", font=("Segoe UI",10,"bold"),
                  padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        tk.Button(bf, text="🗑️ DELETE", command=self._del_sel_user, bg=ERROR, fg="white", font=("Segoe UI",10,"bold"),
                  padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        tk.Button(bf, text="✏️ EDIT", command=self._edit_sel_user, bg=ACCENT, fg="white", font=("Segoe UI",10,"bold"),
                  padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)

        cols = ("Username", "Balance", "Password Hash", "Actions")
        self.user_tree = ttk.Treeview(tab, columns=cols, show="headings", height=15)
        self.user_tree.heading("Username", text="USERNAME")
        self.user_tree.heading("Balance", text="BALANCE ($)")
        self.user_tree.heading("Password Hash", text="PASSWORD HASH (SHA-256)")
        self.user_tree.heading("Actions", text="ACTIONS")
        self.user_tree.column("Username", width=150, anchor="center")
        self.user_tree.column("Balance", width=100, anchor="center")
        self.user_tree.column("Password Hash", width=400, anchor="w")
        self.user_tree.column("Actions", width=200, anchor="center")

        sb = ttk.Scrollbar(tab, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=sb.set)
        self.user_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)
        self.user_tree.bind("<Double-1>", lambda e: self._edit_sel_user())
        self._load_users()

    def _load_users(self):
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)
        for uname, u in self.storage.users.items():
            self.user_tree.insert("", "end", values=(uname, f"${u.balance:.2f}", u.password_hash[:20]+"...", "manage"), tags=(uname,))

    def _del_sel_user(self):
        sel = self.user_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a user first")
            return
        item = self.user_tree.item(sel[0])
        uname = item['values'][0]
        self._del_user(uname)

    def _edit_sel_user(self):
        sel = self.user_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a user first")
            return
        item = self.user_tree.item(sel[0])
        uname = item['values'][0]
        self._edit_user(uname)

    def _del_user(self, uname):
        if uname == "admin":
            messagebox.showerror("Error", "Cannot delete admin")
            return
        if not messagebox.askyesno("Confirm", f"Delete user '{uname}'?"):
            return
        # remove their bookings
        for tid, b in list(self.storage.bookings.items()):
            if b.username == uname:
                del self.storage.bookings[tid]
        del self.storage.users[uname]
        self.storage.save()
        self._load_users()
        self._load_bookings()
        messagebox.showinfo("Success", f"User {uname} deleted")

    def _edit_user(self, uname):
        u = self.storage.get_user(uname)
        if not u: return
        self._edit_dialog(uname, u.balance)

    def _edit_dialog(self, uname, cur_bal):
        d = tk.Toplevel(self)
        d.title(f"Edit User: {uname}")
        d.configure(bg=BG_ROOT)
        d.geometry("400x350")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400)//2
        y = (d.winfo_screenheight() - 350)//2
        d.geometry(f"400x350+{x}+{y}")

        f = tk.Frame(d, bg=BG_CARD, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        tk.Label(f, text=f"EDIT USER: {uname}", font=("Segoe UI",16,"bold"), fg=ACCENT, bg=BG_CARD).pack(pady=(0,20))
        tk.Label(f, text="New Balance ($):", font=("Segoe UI",11), fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0,5))
        be = tk.Entry(f, font=("Segoe UI",12))
        be.insert(0, str(cur_bal))
        be.pack(fill="x", pady=(0,15))
        tk.Label(f, text="New Password (blank=keep):", font=("Segoe UI",10), fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", pady=(0,5))
        pe = tk.Entry(f, font=("Segoe UI",12), show="•")
        pe.pack(fill="x", pady=(0,20))

        def _update():
            try:
                nb = float(be.get())
                u = self.storage.get_user(uname)
                u.balance = nb
                np = pe.get()
                if np:
                    if len(np) < 4:
                        messagebox.showerror("Error", "Password too short")
                        return
                    u.password_hash = hashlib.sha256(np.encode()).hexdigest()
                self.storage.save()
                self._load_users()
                messagebox.showinfo("Success", "User updated")
                d.destroy()
            except:
                messagebox.showerror("Error", "Invalid balance")

        bf = tk.Frame(f, bg=BG_CARD)
        bf.pack(fill="x", pady=10)
        tk.Button(bf, text="💾 SAVE", command=_update, bg=SUCCESS, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        tk.Button(bf, text="✕ CANCEL", command=d.destroy, bg=ERROR, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)

    # ---------- tables tab ----------
    def _tab_tables(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="🎲 TABLES")
        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="Table Management", font=FONT_HEADING, fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        tk.Label(ctrl, text="Click on any table to manage", font=FONT_SMALL, fg=TEXT_DIM, bg=BG_CARD).pack(side="right", padx=20)

        canvas = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        sb = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG_ROOT)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)

        cf = tk.Frame(sf, bg=BG_ROOT)
        cf.pack(fill="both", expand=True)
        self.admin_cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = self._make_admin_card(cf, tid)
            row, col = i//2, i%2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cf.grid_columnconfigure(col, weight=1)
            cf.grid_rowconfigure(row, weight=1)

    def _make_admin_card(self, parent, tid):
        card = tk.Frame(parent, bg=BG_CARD, relief="raised", bd=2)
        hdr = tk.Frame(card, bg=BG_CARD)
        hdr.pack(fill="x", padx=15, pady=10)
        tk.Label(hdr, text=f"TABLE {tid}", font=("Segoe UI",16,"bold"), fg=ACCENT, bg=BG_CARD).pack(side="left")
        b = self.storage.bookings.get(tid)
        status = "🔴 IN USE" if b else "🟢 AVAILABLE"
        color = ERROR if b else SUCCESS
        lbl = tk.Label(hdr, text=status, font=("Segoe UI",10,"bold"), fg=color, bg=BG_CARD)
        lbl.pack(side="right")
        tk.Frame(card, bg=BORDER, height=2).pack(fill="x", padx=10)

        det = tk.Frame(card, bg=BG_CARD)
        det.pack(fill="x", padx=15, pady=10)
        if b:
            for line in [f"👤 User: {b.username}", f"⏱️ Hours: {b.hours}", f"💰 Cost: ${b.cost}", f"🕒 Started: {b.start_time[:16]}"]:
                tk.Label(det, text=line, font=("Segoe UI",10), fg=TEXT, bg=BG_CARD, anchor="w").pack(fill="x", pady=1)
        else:
            tk.Label(det, text="No active booking", font=("Segoe UI",12), fg=TEXT_DIM, bg=BG_CARD).pack(pady=20)

        acts = tk.Frame(card, bg=BG_CARD)
        acts.pack(fill="x", padx=15, pady=10)
        if b:
            tk.Button(acts, text="🔴 FORCE CLOSE", command=lambda t=tid: self._force_close(t),
                      bg=ERROR, fg="white", font=("Segoe UI",10,"bold"), padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=2, fill="x", expand=True)
        tk.Button(acts, text="🔄 RESET", command=lambda t=tid: self._reset_table(t),
                  bg=ACCENT, fg="white", font=("Segoe UI",10,"bold"), padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="right" if b else "left", padx=2, fill="x", expand=True)
        return card

    # ---------- bookings tab ----------
    def _tab_bookings(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="📋 BOOKINGS")
        ctrl = tk.Frame(tab, bg=BG_CARD, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="Booking Management", font=FONT_HEADING, fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        bf = tk.Frame(ctrl, bg=BG_CARD)
        bf.pack(side="right", padx=20)
        tk.Button(bf, text="🗑️ CLEAR ALL", command=self._clear_all_bookings, bg=ERROR, fg="white", font=("Segoe UI",10,"bold"),
                  padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        tk.Button(bf, text="📊 STATS", command=self._stats, bg=ACCENT, fg="white", font=("Segoe UI",10,"bold"),
                  padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)

        cols = ("Table", "User", "Hours", "Cost", "Start Time", "End Time", "Actions")
        self.booking_tree = ttk.Treeview(tab, columns=cols, show="headings", height=15)
        for c in cols: self.booking_tree.heading(c, text=c)
        self.booking_tree.column("Table", width=80, anchor="center")
        self.booking_tree.column("User", width=120, anchor="center")
        self.booking_tree.column("Hours", width=60, anchor="center")
        self.booking_tree.column("Cost", width=80, anchor="center")
        self.booking_tree.column("Start Time", width=150, anchor="center")
        self.booking_tree.column("End Time", width=150, anchor="center")
        self.booking_tree.column("Actions", width=100, anchor="center")
        sb = ttk.Scrollbar(tab, orient="vertical", command=self.booking_tree.yview)
        self.booking_tree.configure(yscrollcommand=sb.set)
        self.booking_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)
        self.booking_tree.bind("<ButtonRelease-1>", self._on_booking_click)
        self._load_bookings()

    def _load_bookings(self):
        for i in self.booking_tree.get_children():
            self.booking_tree.delete(i)
        for tid, b in self.storage.bookings.items():
            et = b.end_time_str if hasattr(b, 'end_time_str') else "N/A"
            self.booking_tree.insert("", "end", values=(tid, b.username, b.hours, f"${b.cost:.2f}", b.start_time[:16], et, "❌ CLOSE"), tags=(tid,))

    def _on_booking_click(self, e):
        sel = self.booking_tree.selection()
        if sel:
            item = self.booking_tree.item(sel[0])
            tid = item['values'][0]
            if messagebox.askyesno("Close Booking", f"Close table {tid}?"):
                self._force_close(tid)

    def _clear_all_bookings(self):
        if messagebox.askyesno("⚠️ WARNING", "Clear ALL bookings? Cannot undo!"):
            self.storage.bookings.clear()
            self.storage.save()
            self._refresh_all()
            messagebox.showinfo("Success", "All bookings cleared")

    # ---------- settings tab ----------
    def _tab_settings(self, nb):
        tab = tk.Frame(nb, bg=BG_ROOT)
        nb.add(tab, text="⚙️ SETTINGS")
        canvas = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        sb = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=BG_ROOT)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        sets = tk.Frame(sf, bg=BG_CARD, padx=30, pady=30)
        sets.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(sets, text="⚙️ SYSTEM SETTINGS", font=("Segoe UI",20,"bold"), fg=ACCENT, bg=BG_CARD).pack(pady=(0,30))

        # rate
        self._mk_section(sets, "💰 RATE SETTINGS", 0)
        rf = tk.Frame(sets, bg=BG_CARD)
        rf.pack(fill="x", pady=10)
        tk.Label(rf, text="Hourly Rate ($):", font=("Segoe UI",12), fg=TEXT, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        self.rate_var = tk.StringVar(value=str(RATE_PER_HOUR))
        re = tk.Entry(rf, textvariable=self.rate_var, font=("Segoe UI",12), width=10, justify="center")
        re.pack(side="left", padx=10)
        tk.Button(rf, text="UPDATE", command=self._update_rate, bg=SUCCESS, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=10)

        # data mgmt
        self._mk_section(sets, "💾 DATA MANAGEMENT", 1)
        df = tk.Frame(sets, bg=BG_CARD)
        df.pack(fill="x", pady=15)
        r1 = tk.Frame(df, bg=BG_CARD)
        r1.pack(fill="x", pady=5)
        tk.Button(r1, text="💾 BACKUP", command=self._backup, bg=ACCENT, fg="white", font=("Segoe UI",11,"bold"),
                  width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        tk.Button(r1, text="📂 RESTORE", command=self._restore, bg=ACCENT, fg="white", font=("Segoe UI",11,"bold"),
                  width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        r2 = tk.Frame(df, bg=BG_CARD)
        r2.pack(fill="x", pady=5)
        tk.Button(r2, text="🗑️ RESET ALL", command=self._reset_all, bg=ERROR, fg="white", font=("Segoe UI",11,"bold"),
                  width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        tk.Button(r2, text="📊 STATS", command=self._stats, bg=WARNING, fg="white", font=("Segoe UI",11,"bold"),
                  width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)

        # stats display
        self._mk_section(sets, "📊 SYSTEM STATISTICS", 2)
        stat_frame = tk.Frame(sets, bg=BG_CARD, relief="solid", bd=1)
        stat_frame.pack(fill="x", pady=10, ipady=10)
        self._update_stats_ui(stat_frame)

    def _mk_section(self, parent, title, idx):
        s = tk.Frame(parent, bg=BG_CARD)
        s.pack(fill="x", pady=(20 if idx>0 else 0, 5))
        tk.Label(s, text=title, font=("Segoe UI",14,"bold"), fg=ACCENT, bg=BG_CARD).pack(anchor="w")
        tk.Frame(s, bg=BORDER, height=2).pack(fill="x", pady=5)

    def _update_stats_ui(self, parent):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        g = tk.Frame(parent, bg=BG_CARD)
        g.pack(fill="x", padx=10, pady=5)
        for label, val, col in [("👥 Total Users:", tu, ACCENT), ("📋 Active Bookings:", tb, ACCENT), ("💰 Total Revenue:", f"${tr:.2f}", SUCCESS)]:
            r = tk.Frame(g, bg=BG_CARD)
            r.pack(fill="x", pady=5)
            tk.Label(r, text=label, font=("Segoe UI",11), fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
            tk.Label(r, text=str(val), font=("Segoe UI",16,"bold"), fg=col, bg=BG_CARD).pack(side="left", padx=20)

    # ---------- common actions ----------
    def _refresh_all(self):
        self._load_users()
        self._load_bookings()
        # rebuild tables tab (simplified: just refresh by recreating? but we keep as is)
        messagebox.showinfo("Success", "Data refreshed")

    def _force_close(self, tid):
        if messagebox.askyesno("Confirm", f"Force close Table {tid}?"):
            if tid in self.storage.bookings:
                del self.storage.bookings[tid]
                self.storage.save()
                self._refresh_all()
                messagebox.showinfo("Success", f"Table {tid} closed")

    def _reset_table(self, tid):
        if tid in self.storage.bookings:
            if messagebox.askyesno("Confirm", f"Reset Table {tid}?"):
                del self.storage.bookings[tid]
                self.storage.save()
                self._refresh_all()
                messagebox.showinfo("Success", f"Table {tid} reset")
        else:
            messagebox.showinfo("Info", f"Table {tid} already empty")

    def _stats(self):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        msg = f"""📊 SYSTEM STATISTICS

👥 Total Users: {tu}
📋 Active Bookings: {tb}
💰 Total Revenue: ${tr:.2f}

🟢 Available Tables: {4 - tb}
🔴 Occupied Tables: {tb}"""
        messagebox.showinfo("Statistics", msg)

    def _update_rate(self):
        try:
            nr = int(self.rate_var.get())
            if nr <= 0: raise ValueError
            global RATE_PER_HOUR
            RATE_PER_HOUR = nr
            messagebox.showinfo("Success", f"Rate updated to ${nr}/hour")
        except:
            messagebox.showerror("Error", "Invalid number")

    def _backup(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bf = f"mahjong_backup_{ts}.json"
        try:
            shutil.copy2(DATA_FILE, bf)
            messagebox.showinfo("Success", f"Backed up to {bf}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")

    def _restore(self):
        fn = filedialog.askopenfilename(title="Select backup", filetypes=[("JSON files","*.json"),("All files","*.*")])
        if fn:
            try:
                with open(fn, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                self.storage._load()
                self._refresh_all()
                messagebox.showinfo("Success", "Restored successfully")
            except Exception as e:
                messagebox.showerror("Error", f"Restore failed: {e}")

    def _reset_all(self):
        if not messagebox.askyesno("⚠️ WARNING", "This will DELETE ALL DATA! Are you sure?"):
            return
        if not messagebox.askyesno("⚠️ FINAL", "Cannot undo. Continue?"):
            return
        self.storage.users.clear()
        self.storage.bookings.clear()
        self.storage._make_test()
        self._refresh_all()
        messagebox.showinfo("Success", "All data reset")

    def _add_user(self):
        d = tk.Toplevel(self)
        d.title("Add New User")
        d.configure(bg=BG_ROOT)
        d.geometry("400x400")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400)//2
        y = (d.winfo_screenheight() - 400)//2
        d.geometry(f"400x400+{x}+{y}")

        f = tk.Frame(d, bg=BG_CARD, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="➕ ADD NEW USER", font=("Segoe UI",16,"bold"), fg=ACCENT, bg=BG_CARD).pack(pady=(0,20))
        tk.Label(f, text="Username:", font=("Segoe UI",11), fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0,5))
        ue = tk.Entry(f, font=("Segoe UI",12))
        ue.pack(fill="x", pady=(0,15))
        tk.Label(f, text="Password:", font=("Segoe UI",11), fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0,5))
        pe = tk.Entry(f, font=("Segoe UI",12), show="•")
        pe.pack(fill="x", pady=(0,15))
        tk.Label(f, text="Initial Balance ($):", font=("Segoe UI",11), fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0,5))
        be = tk.Entry(f, font=("Segoe UI",12))
        be.insert(0, "0")
        be.pack(fill="x", pady=(0,20))

        def _do_add():
            un = ue.get().strip()
            pw = pe.get()
            try:
                bal = float(be.get())
            except:
                messagebox.showerror("Error", "Invalid balance")
                return
            if not un or not pw:
                messagebox.showerror("Error", "Fill all fields")
                return
            ok, msg = self.storage.register(un, pw)
            if ok:
                u = self.storage.get_user(un)
                if u: u.balance = bal
                self.storage.save()
                self._load_users()
                messagebox.showinfo("Success", f"User {un} created")
                d.destroy()
            else:
                messagebox.showerror("Error", msg)

        bf = tk.Frame(f, bg=BG_CARD)
        bf.pack(fill="x", pady=10)
        tk.Button(bf, text="✅ CREATE", command=_do_add, bg=SUCCESS, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        tk.Button(bf, text="✕ CANCEL", command=d.destroy, bg=ERROR, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)