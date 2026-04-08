import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from config import *
from datetime import datetime
import hashlib, json, shutil

class AdminWindow(tk.Toplevel):
    def __init__(self, master, storage):
        tk.Toplevel.__init__(self, master)
        self.master = master
        self.storage = storage

        self.title("Admin Dashboard")
        self.configure(bg=bgroot)
        self.geometry("1100x700")
        self.resizable(True, True)

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        xp = (sw - 1100)//2
        yp = (sh - 700)//2
        self.geometry("1100x700+%d+%d" % (xp, yp))

        self.transient(master)
        self.grab_set()

        main = tk.Frame(self, bg=bgroot)
        main.pack(fill="both", expand=True)

        head = tk.Frame(main, bg=bgcard, height=70)
        head.pack(fill="x")
        head.pack_propagate(False)
        tk.Label(head, text="ADMIN PANEL", font=fonttitle, fg=accent, bg=bgcard).pack(side="left", padx=20, pady=15)
        btn_frame = tk.Frame(head, bg=bgcard)
        btn_frame.pack(side="right", padx=20)
        tk.Button(btn_frame, text="Refresh", command=self.refresh_all, bg=accent, fg="white", font=fontbtn).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Backup", command=self.backup, bg=success, fg="white", font=fontbtn).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Stats", command=self.stats, bg=warning, fg="white", font=fontbtn).pack(side="left", padx=5)

        nb = ttk.Notebook(main)
        nb.pack(fill="both", expand=True, padx=10, pady=10)

        # Users tab
        self.user_tab = tk.Frame(nb, bg=bgroot)
        nb.add(self.user_tab, text="Users")
        self._make_user_tab()

        # Tables tab (recreated on refresh)
        self.tables_tab = None
        self._make_tables_tab(nb)

        # Bookings tab
        self.book_tab = tk.Frame(nb, bg=bgroot)
        nb.add(self.book_tab, text="Bookings")
        self._make_bookings_tab()

        # Settings tab
        self.sett_tab = tk.Frame(nb, bg=bgroot)
        nb.add(self.sett_tab, text="Settings")
        self._make_settings_tab()

        self.protocol("WM_DELETE_WINDOW", self.destroy)

    def _make_user_tab(self):
        ctrl = tk.Frame(self.user_tab, bg=bgcard, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="User Management", font=fontheading, fg=accent, bg=bgcard).pack(side="left", padx=20, pady=15)
        bf = tk.Frame(ctrl, bg=bgcard)
        bf.pack(side="right", padx=20)
        tk.Button(bf, text="Add", command=self.add_user, bg=success, fg="white", font=fontbtn).pack(side="left", padx=5)
        tk.Button(bf, text="Delete", command=self.del_selected_user, bg=error, fg="white", font=fontbtn).pack(side="left", padx=5)
        tk.Button(bf, text="Edit", command=self.edit_selected_user, bg=accent, fg="white", font=fontbtn).pack(side="left", padx=5)

        cols = ("Username", "Balance", "Password Hash")
        self.user_tree = ttk.Treeview(self.user_tab, columns=cols, show="headings", height=15)
        self.user_tree.heading("Username", text="USERNAME")
        self.user_tree.heading("Balance", text="BALANCE ($)")
        self.user_tree.heading("Password Hash", text="PASSWORD HASH")
        self.user_tree.column("Username", width=150)
        self.user_tree.column("Balance", width=100)
        self.user_tree.column("Password Hash", width=400)
        self.user_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb = ttk.Scrollbar(self.user_tab, orient="vertical", command=self.user_tree.yview)
        self.user_tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)
        self._load_users()

    def _make_tables_tab(self, nb):
        if self.tables_tab:
            nb.forget(self.tables_tab)
        self.tables_tab = tk.Frame(nb, bg=bgroot)
        nb.insert(1, self.tables_tab, text="Tables")
        ctrl = tk.Frame(self.tables_tab, bg=bgcard, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="Table Management", font=fontheading, fg=accent, bg=bgcard).pack(side="left", padx=20, pady=15)

        canvas = tk.Canvas(self.tables_tab, bg=bgroot, highlightthickness=0)
        sb = tk.Scrollbar(self.tables_tab, orient="vertical", command=canvas.yview)
        sf = tk.Frame(canvas, bg=bgroot)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0,0), window=sf, anchor="nw")
        canvas.configure(yscrollcommand=sb.set)
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)

        for i, tid in enumerate(tableids):
            self._add_admin_card(sf, tid)

    def _add_admin_card(self, parent, tid):
        card = tk.Frame(parent, bg=bgcard, relief="raised", bd=2)
        card.pack(fill="x", padx=10, pady=10)
        hdr = tk.Frame(card, bg=bgcard)
        hdr.pack(fill="x", padx=15, pady=10)
        tk.Label(hdr, text="TABLE %s" % tid, font=("Segoe UI",16,"bold"), fg=accent, bg=bgcard).pack(side="left")
        b = self.storage.bookings.get(tid)
        status = "IN USE" if b else "AVAILABLE"
        color = error if b else success
        tk.Label(hdr, text=status, font=("Segoe UI",10,"bold"), fg=color, bg=bgcard).pack(side="right")
        tk.Frame(card, bg=border, height=2).pack(fill="x", padx=10)

        det = tk.Frame(card, bg=bgcard)
        det.pack(fill="x", padx=15, pady=10)
        if b:
            for line in ["User: %s" % b.username, "Hours: %d" % b.hours, "Cost: $%.2f" % b.cost, "Started: %s" % b.start_time[:16]]:
                tk.Label(det, text=line, font=("Segoe UI",10), fg=text, bg=bgcard, anchor="w").pack(fill="x", pady=1)
        else:
            tk.Label(det, text="No active booking", font=("Segoe UI",12), fg=textdim, bg=bgcard).pack(pady=20)

        acts = tk.Frame(card, bg=bgcard)
        acts.pack(fill="x", padx=15, pady=10)
        if b:
            tk.Button(acts, text="Force Close", command=lambda t=tid: self.force_close(t),
                      bg=error, fg="white", font=fontbtn).pack(side="left", padx=2, fill="x", expand=True)
        tk.Button(acts, text="Reset", command=lambda t=tid: self.reset_table(t),
                  bg=accent, fg="white", font=fontbtn).pack(side="right" if b else "left", padx=2, fill="x", expand=True)

    def _make_bookings_tab(self):
        ctrl = tk.Frame(self.book_tab, bg=bgcard, height=60)
        ctrl.pack(fill="x", pady=(0,10))
        ctrl.pack_propagate(False)
        tk.Label(ctrl, text="Booking Management", font=fontheading, fg=accent, bg=bgcard).pack(side="left", padx=20, pady=15)
        tk.Button(ctrl, text="Clear All", command=self.clear_all_bookings, bg=error, fg="white", font=fontbtn).pack(side="right", padx=20)

        cols = ("Table", "User", "Hours", "Cost", "Start Time", "End Time")
        self.booking_tree = ttk.Treeview(self.book_tab, columns=cols, show="headings", height=15)
        for c in cols: self.booking_tree.heading(c, text=c)
        self.booking_tree.column("Table", width=80)
        self.booking_tree.column("User", width=120)
        self.booking_tree.column("Hours", width=60)
        self.booking_tree.column("Cost", width=80)
        self.booking_tree.column("Start Time", width=150)
        self.booking_tree.column("End Time", width=150)
        self.booking_tree.pack(side="left", fill="both", expand=True, padx=(10,0), pady=10)
        sb = ttk.Scrollbar(self.book_tab, orient="vertical", command=self.booking_tree.yview)
        self.booking_tree.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y", padx=(0,10), pady=10)
        self._load_bookings()

    def _make_settings_tab(self):
        sets = tk.Frame(self.sett_tab, bg=bgcard, padx=30, pady=30)
        sets.pack(fill="both", expand=True, padx=20, pady=20)
        tk.Label(sets, text="SYSTEM SETTINGS", font=("Segoe UI",20,"bold"), fg=accent, bg=bgcard).pack(pady=(0,30))

        # Rate
        rf = tk.Frame(sets, bg=bgcard)
        rf.pack(fill="x", pady=10)
        tk.Label(rf, text="Hourly Rate ($):", font=("Segoe UI",12), fg=text, bg=bgcard).pack(side="left")
        self.rate_var = tk.StringVar(value=str(self.storage.rate))
        re = tk.Entry(rf, textvariable=self.rate_var, font=("Segoe UI",12), width=10)
        re.pack(side="left", padx=10)
        tk.Button(rf, text="Update", command=self.update_rate, bg=success, fg="white", font=fontbtn).pack(side="left", padx=10)

        # Data management
        df = tk.Frame(sets, bg=bgcard)
        df.pack(fill="x", pady=20)
        tk.Button(df, text="Backup Data", command=self.backup, bg=accent, fg="white", font=fontbtn, width=20).pack(side="left", padx=5, expand=True)
        tk.Button(df, text="Restore Data", command=self.restore, bg=accent, fg="white", font=fontbtn, width=20).pack(side="left", padx=5, expand=True)
        tk.Button(df, text="Reset All", command=self.reset_all, bg=error, fg="white", font=fontbtn, width=20).pack(side="left", padx=5, expand=True)

        # Stats
        stat_frame = tk.Frame(sets, bg=bgcard, relief="solid", bd=1)
        stat_frame.pack(fill="x", pady=20, ipady=10)
        self._update_stats_ui(stat_frame)

    def _update_stats_ui(self, parent):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        for label, val in [("Total Users:", tu), ("Active Bookings:", tb), ("Total Revenue:", "$%.2f" % tr)]:
            r = tk.Frame(parent, bg=bgcard)
            r.pack(fill="x", pady=5)
            tk.Label(r, text=label, font=("Segoe UI",11), fg=text, bg=bgcard, width=20, anchor="w").pack(side="left")
            tk.Label(r, text=str(val), font=("Segoe UI",16,"bold"), fg=accent, bg=bgcard).pack(side="left", padx=20)

    def _load_users(self):
        for i in self.user_tree.get_children():
            self.user_tree.delete(i)
        for uname, u in self.storage.users.items():
            self.user_tree.insert("", "end", values=(uname, "$%.2f" % u.balance, u.password_hash[:20]+"..."))

    def _load_bookings(self):
        for i in self.booking_tree.get_children():
            self.booking_tree.delete(i)
        for tid, b in self.storage.bookings.items():
            et = b.end_time_str if hasattr(b, 'end_time_str') else "N/A"
            self.booking_tree.insert("", "end", values=(tid, b.username, b.hours, "$%.2f" % b.cost, b.start_time[:16], et))

    def refresh_all(self):
        self._load_users()
        self._load_bookings()
        # rebuild tables tab
        nb = self.master.nametowidget(self.tables_tab.master)
        self._make_tables_tab(nb)
        messagebox.showinfo("Success", "Data refreshed")

    def force_close(self, tid):
        if messagebox.askyesno("Confirm", "Force close Table %s?" % tid):
            if tid in self.storage.bookings:
                del self.storage.bookings[tid]
                self.storage.save()
                self.refresh_all()

    def reset_table(self, tid):
        if tid in self.storage.bookings:
            if messagebox.askyesno("Confirm", "Reset Table %s?" % tid):
                del self.storage.bookings[tid]
                self.storage.save()
                self.refresh_all()
        else:
            messagebox.showinfo("Info", "Table %s already empty" % tid)

    def stats(self):
        tu = len(self.storage.users)
        tb = len(self.storage.bookings)
        tr = sum(b.cost for b in self.storage.bookings.values())
        msg = "Total Users: %d\nActive Bookings: %d\nTotal Revenue: $%.2f\nAvailable Tables: %d" % (tu, tb, tr, 4-tb)
        messagebox.showinfo("Statistics", msg)

    def update_rate(self):
        try:
            nr = int(self.rate_var.get())
            if nr <= 0: raise ValueError
            self.storage.rate = nr
            self.storage.save()
            messagebox.showinfo("Success", "Rate updated to $%d/hour" % nr)
        except:
            messagebox.showerror("Error", "Invalid number")

    def backup(self):
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        bf = "mahjong_backup_%s.json" % ts
        try:
            shutil.copy2(datafile, bf)
            messagebox.showinfo("Success", "Backed up to %s" % bf)
        except Exception as e:
            messagebox.showerror("Error", "Backup failed: %s" % e)

    def restore(self):
        fn = filedialog.askopenfilename(title="Select backup", filetypes=[("JSON files","*.json")])
        if fn:
            try:
                with open(fn, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                with open(datafile, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=2)
                self.storage._load()
                self.refresh_all()
                messagebox.showinfo("Success", "Restored successfully")
            except Exception as e:
                messagebox.showerror("Error", "Restore failed: %s" % e)

    def reset_all(self):
        if not messagebox.askyesno("WARNING", "Delete ALL data? Are you sure?"):
            return
        if not messagebox.askyesno("FINAL", "Cannot undo. Continue?"):
            return
        self.storage.users.clear()
        self.storage.bookings.clear()
        self.storage._make_test()
        self.refresh_all()
        messagebox.showinfo("Success", "All data reset")

    def add_user(self):
        d = tk.Toplevel(self)
        d.title("Add New User")
        d.configure(bg=bgroot)
        d.geometry("400x400")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400)//2
        y = (d.winfo_screenheight() - 400)//2
        d.geometry("400x400+%d+%d" % (x, y))

        f = tk.Frame(d, bg=bgcard, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="ADD NEW USER", font=("Segoe UI",16,"bold"), fg=accent, bg=bgcard).pack(pady=(0,20))
        tk.Label(f, text="Username:", font=("Segoe UI",11), fg=text, bg=bgcard).pack(anchor="w", pady=(0,5))
        ue = tk.Entry(f, font=("Segoe UI",12))
        ue.pack(fill="x", pady=(0,15))
        tk.Label(f, text="Password:", font=("Segoe UI",11), fg=text, bg=bgcard).pack(anchor="w", pady=(0,5))
        pe = tk.Entry(f, font=("Segoe UI",12), show="•")
        pe.pack(fill="x", pady=(0,15))
        tk.Label(f, text="Initial Balance ($):", font=("Segoe UI",11), fg=text, bg=bgcard).pack(anchor="w", pady=(0,5))
        be = tk.Entry(f, font=("Segoe UI",12))
        be.insert(0, "0")
        be.pack(fill="x", pady=(0,20))

        def do_add():
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
                messagebox.showinfo("Success", "User %s created" % un)
                d.destroy()
            else:
                messagebox.showerror("Error", msg)

        bf = tk.Frame(f, bg=bgcard)
        bf.pack(fill="x", pady=10)
        tk.Button(bf, text="CREATE", command=do_add, bg=success, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        tk.Button(bf, text="CANCEL", command=d.destroy, bg=error, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)

    def del_selected_user(self):
        sel = self.user_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a user first")
            return
        item = self.user_tree.item(sel[0])
        uname = item['values'][0]
        if uname == "admin":
            messagebox.showerror("Error", "Cannot delete admin")
            return
        if not messagebox.askyesno("Confirm", "Delete user '%s'?" % uname):
            return
        for tid, b in list(self.storage.bookings.items()):
            if b.username == uname:
                del self.storage.bookings[tid]
        del self.storage.users[uname]
        self.storage.save()
        self.refresh_all()
        messagebox.showinfo("Success", "User %s deleted" % uname)

    def edit_selected_user(self):
        sel = self.user_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a user first")
            return
        item = self.user_tree.item(sel[0])
        uname = item['values'][0]
        u = self.storage.get_user(uname)
        if not u: return
        self._edit_dialog(uname, u.balance)

    def _edit_dialog(self, uname, cur_bal):
        d = tk.Toplevel(self)
        d.title("Edit User: %s" % uname)
        d.configure(bg=bgroot)
        d.geometry("400x350")
        d.resizable(False, False)
        d.transient(self)
        d.grab_set()
        d.update_idletasks()
        x = (d.winfo_screenwidth() - 400)//2
        y = (d.winfo_screenheight() - 350)//2
        d.geometry("400x350+%d+%d" % (x, y))

        f = tk.Frame(d, bg=bgcard, padx=25, pady=25)
        f.pack(fill="both", expand=True)
        tk.Label(f, text="EDIT USER: %s" % uname, font=("Segoe UI",16,"bold"), fg=accent, bg=bgcard).pack(pady=(0,20))
        tk.Label(f, text="New Balance ($):", font=("Segoe UI",11), fg=text, bg=bgcard).pack(anchor="w", pady=(0,5))
        be = tk.Entry(f, font=("Segoe UI",12))
        be.insert(0, str(cur_bal))
        be.pack(fill="x", pady=(0,15))
        tk.Label(f, text="New Password (blank=keep):", font=("Segoe UI",10), fg=textdim, bg=bgcard).pack(anchor="w", pady=(0,5))
        pe = tk.Entry(f, font=("Segoe UI",12), show="•")
        pe.pack(fill="x", pady=(0,20))

        def update():
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

        bf = tk.Frame(f, bg=bgcard)
        bf.pack(fill="x", pady=10)
        tk.Button(bf, text="SAVE", command=update, bg=success, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        tk.Button(bf, text="CANCEL", command=d.destroy, bg=error, fg="white", font=("Segoe UI",11,"bold"),
                  padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)

    def clear_all_bookings(self):
        if messagebox.askyesno("WARNING", "Clear ALL bookings? Cannot undo!"):
            self.storage.bookings.clear()
            self.storage.save()
            self.refresh_all()
            messagebox.showinfo("Success", "All bookings cleared")