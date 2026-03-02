# admin_window.py
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
        
        # Center window
        self.update_idletasks()
        x = (self.winfo_screenwidth() - 1100) // 2
        y = (self.winfo_screenheight() - 700) // 2
        self.geometry(f"1100x700+{x}+{y}")
        
        self.transient(master)
        self.grab_set()
        
        self._build_ui()
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        
        # Fade in animation
        self.after(100, lambda: fade_in(self))
        
    def _on_close(self):
        self.destroy()
        
    def _build_ui(self):
        # Main container
        main = tk.Frame(self, bg=BG_ROOT)
        main.pack(fill="both", expand=True)
        
        # Header with title and quick actions
        header = tk.Frame(main, bg=BG_CARD, height=70)
        header.pack(fill="x")
        header.pack_propagate(False)
        
        # Left side - Title
        title_frame = tk.Frame(header, bg=BG_CARD)
        title_frame.pack(side="left", padx=20, pady=15)
        
        tk.Label(title_frame, text="👑 ADMIN DASHBOARD", font=FONT_TITLE,
                fg=ACCENT, bg=BG_CARD).pack(side="left")
        
        # Right side - Quick action buttons
        action_frame = tk.Frame(header, bg=BG_CARD)
        action_frame.pack(side="right", padx=20, pady=10)
        
        # Quick action buttons
        tk.Button(action_frame, text="🔄 Refresh All", command=self._refresh_all,
                 bg=ACCENT, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="💾 Backup Now", command=self._backup_data,
                 bg=SUCCESS, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(action_frame, text="📊 Statistics", command=self._show_statistics,
                 bg=WARNING, fg="white", font=FONT_BTN,
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        # Create notebook for tabs
        notebook = ttk.Notebook(main)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Style the notebook
        style = ttk.Style()
        style.configure("TNotebook", background=BG_ROOT)
        style.configure("TNotebook.Tab", padding=[15, 8], font=("Segoe UI", 10, "bold"))
        
        # Create tabs
        self._create_users_tab(notebook)
        self._create_tables_tab(notebook)
        self._create_bookings_tab(notebook)
        self._create_settings_tab(notebook)
        
    def _create_users_tab(self, notebook):
        """Users management tab with enhanced UI"""
        tab = tk.Frame(notebook, bg=BG_ROOT)
        notebook.add(tab, text="👥 USER MANAGEMENT")
        
        # Top control panel with action buttons
        control = tk.Frame(tab, bg=BG_CARD, height=60)
        control.pack(fill="x", pady=(0, 10))
        control.pack_propagate(False)
        
        tk.Label(control, text="User Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        # Action buttons
        btn_frame = tk.Frame(control, bg=BG_CARD)
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="➕ ADD NEW USER", command=self._add_user_dialog,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="🗑️ DELETE SELECTED", command=self._delete_selected_user,
                 bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="✏️ EDIT SELECTED", command=self._edit_selected_user,
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        # Users table with better visibility
        columns = ("Username", "Balance", "Password Hash", "Actions")
        self.users_tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)
        
        # Define headings
        self.users_tree.heading("Username", text="USERNAME")
        self.users_tree.heading("Balance", text="BALANCE ($)")
        self.users_tree.heading("Password Hash", text="PASSWORD HASH (SHA-256)")
        self.users_tree.heading("Actions", text="QUICK ACTIONS")
        
        # Set column widths
        self.users_tree.column("Username", width=150, anchor="center")
        self.users_tree.column("Balance", width=100, anchor="center")
        self.users_tree.column("Password Hash", width=400, anchor="w")
        self.users_tree.column("Actions", width=200, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.users_tree.yview)
        self.users_tree.configure(yscrollcommand=scrollbar.set)
        
        self.users_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Bind double-click to edit
        self.users_tree.bind("<Double-1>", self._edit_user)
        
        # Load users
        self._load_users()
        
    def _create_tables_tab(self, notebook):
        """Tables management tab with better card layout"""
        tab = tk.Frame(notebook, bg=BG_ROOT)
        notebook.add(tab, text="🎲 TABLE MANAGEMENT")
        
        # Top control panel
        control = tk.Frame(tab, bg=BG_CARD, height=60)
        control.pack(fill="x", pady=(0, 10))
        control.pack_propagate(False)
        
        tk.Label(control, text="Table Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        tk.Label(control, text="Click on any table to manage", font=FONT_SMALL,
                fg=TEXT_DIM, bg=BG_CARD).pack(side="right", padx=20)
        
        # Create scrollable frame for table cards
        canvas = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_ROOT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Create table cards in grid
        cards_frame = tk.Frame(scrollable_frame, bg=BG_ROOT)
        cards_frame.pack(fill="both", expand=True)
        
        self.table_cards = {}
        for i, tid in enumerate(TABLE_IDS):
            card = self._create_table_status_card(cards_frame, tid)
            row = i // 2
            col = i % 2
            card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
            cards_frame.grid_columnconfigure(col, weight=1)
            cards_frame.grid_rowconfigure(row, weight=1)
            
    def _create_table_status_card(self, parent, table_id):
        """Create a beautiful table status card with buttons"""
        card = tk.Frame(parent, bg=BG_CARD, relief="raised", bd=2)
        
        # Header with table number and status
        header = tk.Frame(card, bg=BG_CARD)
        header.pack(fill="x", padx=15, pady=10)
        
        tk.Label(header, text=f"TABLE {table_id}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left")
        
        # Status indicator
        booking = self.storage.bookings.get(table_id)
        if booking:
            status_text = "🔴 IN USE"
            status_color = ERROR
        else:
            status_text = "🟢 AVAILABLE"
            status_color = SUCCESS
        
        status_label = tk.Label(header, text=status_text, font=("Segoe UI", 10, "bold"),
                               fg=status_color, bg=BG_CARD)
        status_label.pack(side="right")
        
        # Separator
        tk.Frame(card, bg=BORDER, height=2).pack(fill="x", padx=10)
        
        # Details section
        details = tk.Frame(card, bg=BG_CARD)
        details.pack(fill="x", padx=15, pady=10)
        
        if booking:
            info = [
                f"👤 User: {booking.username}",
                f"⏱️ Hours: {booking.hours}",
                f"💰 Cost: ${booking.cost}",
                f"🕒 Started: {booking.start_time[:16]}"
            ]
            for line in info:
                tk.Label(details, text=line, font=("Segoe UI", 10),
                        fg=TEXT, bg=BG_CARD, anchor="w").pack(fill="x", pady=1)
        else:
            tk.Label(details, text="No active booking", font=("Segoe UI", 12),
                    fg=TEXT_DIM, bg=BG_CARD).pack(pady=20)
        
        # Action buttons
        actions = tk.Frame(card, bg=BG_CARD)
        actions.pack(fill="x", padx=15, pady=10)
        
        if booking:
            tk.Button(actions, text="🔴 FORCE CLOSE", 
                     command=lambda t=table_id: self._force_close_table(t),
                     bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                     padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=2, fill="x", expand=True)
        
        tk.Button(actions, text="🔄 RESET TABLE", 
                 command=lambda t=table_id: self._reset_table(t),
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=10, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="right" if booking else "left", padx=2, fill="x", expand=True)
        
        return card
        
    def _create_bookings_tab(self, notebook):
        """Bookings management tab with action buttons"""
        tab = tk.Frame(notebook, bg=BG_ROOT)
        notebook.add(tab, text="📋 BOOKING MANAGEMENT")
        
        # Control panel
        control = tk.Frame(tab, bg=BG_CARD, height=60)
        control.pack(fill="x", pady=(0, 10))
        control.pack_propagate(False)
        
        tk.Label(control, text="Booking Management", font=FONT_HEADING,
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20, pady=15)
        
        # Action buttons
        btn_frame = tk.Frame(control, bg=BG_CARD)
        btn_frame.pack(side="right", padx=20)
        
        tk.Button(btn_frame, text="🗑️ CLEAR ALL BOOKINGS", command=self._clear_all_bookings,
                 bg=ERROR, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        tk.Button(btn_frame, text="📊 VIEW STATISTICS", command=self._show_booking_stats,
                 bg=ACCENT, fg="white", font=("Segoe UI", 10, "bold"),
                 padx=15, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5)
        
        # Bookings table
        columns = ("Table", "User", "Hours", "Cost", "Start Time", "End Time", "Actions")
        self.bookings_tree = ttk.Treeview(tab, columns=columns, show="headings", height=15)
        
        # Define headings
        self.bookings_tree.heading("Table", text="TABLE")
        self.bookings_tree.heading("User", text="USER")
        self.bookings_tree.heading("Hours", text="HOURS")
        self.bookings_tree.heading("Cost", text="COST ($)")
        self.bookings_tree.heading("Start Time", text="START TIME")
        self.bookings_tree.heading("End Time", text="END TIME")
        self.bookings_tree.heading("Actions", text="ACTIONS")
        
        # Set column widths
        self.bookings_tree.column("Table", width=80, anchor="center")
        self.bookings_tree.column("User", width=120, anchor="center")
        self.bookings_tree.column("Hours", width=60, anchor="center")
        self.bookings_tree.column("Cost", width=80, anchor="center")
        self.bookings_tree.column("Start Time", width=150, anchor="center")
        self.bookings_tree.column("End Time", width=150, anchor="center")
        self.bookings_tree.column("Actions", width=100, anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(tab, orient="vertical", command=self.bookings_tree.yview)
        self.bookings_tree.configure(yscrollcommand=scrollbar.set)
        
        self.bookings_tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 10), pady=10)
        
        # Bind click to show actions
        self.bookings_tree.bind("<ButtonRelease-1>", self._on_booking_click)
        
        # Load bookings
        self._load_bookings()
        
    def _create_settings_tab(self, notebook):
        """Settings tab with organized buttons"""
        tab = tk.Frame(notebook, bg=BG_ROOT)
        notebook.add(tab, text="⚙️ SYSTEM SETTINGS")
        
        # Create scrollable frame for settings
        canvas = tk.Canvas(tab, bg=BG_ROOT, highlightthickness=0)
        scrollbar = tk.Scrollbar(tab, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=BG_ROOT)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Main settings container
        settings = tk.Frame(scrollable_frame, bg=BG_CARD, padx=30, pady=30)
        settings.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        tk.Label(settings, text="⚙️ SYSTEM SETTINGS", font=("Segoe UI", 20, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 30))
        
        # Rate Settings Section
        self._create_settings_section(settings, "💰 RATE SETTINGS", 0)
        
        rate_frame = tk.Frame(settings, bg=BG_CARD)
        rate_frame.pack(fill="x", pady=10)
        
        tk.Label(rate_frame, text="Hourly Rate ($):", font=("Segoe UI", 12),
                fg=TEXT, bg=BG_CARD, width=15, anchor="w").pack(side="left")
        
        self.rate_var = tk.StringVar(value=str(RATE_PER_HOUR))
        rate_entry = tk.Entry(rate_frame, textvariable=self.rate_var, 
                             font=("Segoe UI", 12), width=10, justify="center")
        rate_entry.pack(side="left", padx=10)
        
        tk.Button(rate_frame, text="UPDATE RATE", command=self._update_rate,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=5, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=10)
        
        # Data Management Section
        self._create_settings_section(settings, "💾 DATA MANAGEMENT", 1)
        
        data_frame = tk.Frame(settings, bg=BG_CARD)
        data_frame.pack(fill="x", pady=15)
        
        # First row
        row1 = tk.Frame(data_frame, bg=BG_CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Button(row1, text="💾 BACKUP DATA", command=self._backup_data,
                 bg=ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        tk.Button(row1, text="📂 RESTORE DATA", command=self._restore_data,
                 bg=ACCENT, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        # Second row
        row2 = tk.Frame(data_frame, bg=BG_CARD)
        row2.pack(fill="x", pady=5)
        
        tk.Button(row2, text="🗑️ RESET ALL DATA", command=self._reset_all_data,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        tk.Button(row2, text="📊 VIEW STATISTICS", command=self._show_statistics,
                 bg=WARNING, fg="white", font=("Segoe UI", 11, "bold"),
                 width=20, height=2, cursor="hand2", relief="raised", bd=2).pack(side="left", padx=5, expand=True)
        
        # Statistics Section
        self._create_settings_section(settings, "📊 SYSTEM STATISTICS", 2)
        
        stats_frame = tk.Frame(settings, bg=BG_CARD, relief="solid", bd=1)
        stats_frame.pack(fill="x", pady=10, ipady=10)
        
        self._update_statistics_display(stats_frame)
        
    def _create_settings_section(self, parent, title, index):
        """Create a section header for settings"""
        section = tk.Frame(parent, bg=BG_CARD)
        section.pack(fill="x", pady=(20 if index > 0 else 0, 5))
        
        tk.Label(section, text=title, font=("Segoe UI", 14, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(anchor="w")
        
        tk.Frame(section, bg=BORDER, height=2).pack(fill="x", pady=5)
        
    def _update_statistics_display(self, parent):
        """Update and display statistics"""
        total_users = len(self.storage.users)
        total_bookings = len(self.storage.bookings)
        total_revenue = sum(b.cost for b in self.storage.bookings.values())
        
        stats_grid = tk.Frame(parent, bg=BG_CARD)
        stats_grid.pack(fill="x", padx=10, pady=5)
        
        # Row 1
        row1 = tk.Frame(stats_grid, bg=BG_CARD)
        row1.pack(fill="x", pady=5)
        
        tk.Label(row1, text=f"👥 Total Users:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(row1, text=f"{total_users}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20)
        
        # Row 2
        row2 = tk.Frame(stats_grid, bg=BG_CARD)
        row2.pack(fill="x", pady=5)
        
        tk.Label(row2, text=f"📋 Active Bookings:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(row2, text=f"{total_bookings}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(side="left", padx=20)
        
        # Row 3
        row3 = tk.Frame(stats_grid, bg=BG_CARD)
        row3.pack(fill="x", pady=5)
        
        tk.Label(row3, text=f"💰 Total Revenue:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD, width=20, anchor="w").pack(side="left")
        tk.Label(row3, text=f"${total_revenue:.2f}", font=("Segoe UI", 16, "bold"),
                fg=SUCCESS, bg=BG_CARD).pack(side="left", padx=20)
        
    def _load_users(self):
        """Load users into treeview"""
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        
        for username, user in self.storage.users.items():
            # Create action buttons frame
            actions_frame = tk.Frame(self.users_tree, bg=BG_CARD)
            
            edit_btn = tk.Button(actions_frame, text="✏️", font=("Segoe UI", 10),
                                command=lambda u=username: self._edit_user_by_name(u),
                                bg=ACCENT, fg="white", width=3, cursor="hand2")
            edit_btn.pack(side="left", padx=2)
            
            delete_btn = tk.Button(actions_frame, text="🗑️", font=("Segoe UI", 10),
                                  command=lambda u=username: self._delete_user_by_name(u),
                                  bg=ERROR, fg="white", width=3, cursor="hand2")
            delete_btn.pack(side="left", padx=2)
            
            self.users_tree.insert("", "end", values=(
                username,
                f"${user.balance:.2f}",
                user.password_hash[:20] + "...",
                "Click to manage"
            ), tags=(username,))
            
    def _load_bookings(self):
        """Load bookings into treeview"""
        for item in self.bookings_tree.get_children():
            self.bookings_tree.delete(item)
        
        for table_id, booking in self.storage.bookings.items():
            end_time = booking.end_time_str if hasattr(booking, 'end_time_str') else "N/A"
            self.bookings_tree.insert("", "end", values=(
                table_id,
                booking.username,
                booking.hours,
                f"${booking.cost:.2f}",
                booking.start_time[:16],
                end_time,
                "❌ CLOSE"
            ), tags=(table_id,))
            
    def _refresh_all(self):
        """Refresh all tabs"""
        self._load_users()
        self._load_bookings()
        messagebox.showinfo("Success", "✨ All data refreshed successfully!")
        
    def _delete_selected_user(self):
        """Delete the selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to delete")
            return
        
        item = self.users_tree.item(selection[0])
        username = item['values'][0]
        self._delete_user_by_name(username)
        
    def _edit_selected_user(self):
        """Edit the selected user"""
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a user to edit")
            return
        
        item = self.users_tree.item(selection[0])
        username = item['values'][0]
        self._edit_user_by_name(username)
        
    def _delete_user_by_name(self, username):
        """Delete user by username"""
        if username == "admin":
            messagebox.showerror("Error", "❌ Cannot delete admin user!")
            return
            
        if messagebox.askyesno("Confirm Delete", f"Delete user '{username}'?"):
            # Check for active bookings
            user_bookings = [b for b in self.storage.bookings.values() if b.username == username]
            if user_bookings:
                for table_id, booking in list(self.storage.bookings.items()):
                    if booking.username == username:
                        del self.storage.bookings[table_id]
            
            del self.storage.users[username]
            self.storage.save()
            self._load_users()
            self._load_bookings()
            messagebox.showinfo("Success", f"✅ User '{username}' deleted!")
            
    def _edit_user_by_name(self, username):
        """Edit user by username"""
        user = self.storage.get_user(username)
        if user:
            self._edit_user_dialog(username, user.balance)
            
    def _edit_user_dialog(self, username, current_balance):
        """Open edit user dialog"""
        dialog = tk.Toplevel(self)
        dialog.title(f"Edit User: {username}")
        dialog.configure(bg=BG_ROOT)
        dialog.geometry("400x350")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 350) // 2
        dialog.geometry(f"400x350+{x}+{y}")
        
        # Form
        frame = tk.Frame(dialog, bg=BG_CARD, padx=25, pady=25)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text=f"EDIT USER: {username}", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 20))
        
        # Balance
        tk.Label(frame, text="New Balance ($):", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        balance_entry = tk.Entry(frame, font=("Segoe UI", 12))
        balance_entry.insert(0, str(current_balance))
        balance_entry.pack(fill="x", pady=(0, 15))
        
        # Password
        tk.Label(frame, text="New Password (leave blank to keep):", font=("Segoe UI", 10),
                fg=TEXT_DIM, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(frame, font=("Segoe UI", 12), show="•")
        password_entry.pack(fill="x", pady=(0, 20))
        
        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_CARD)
        btn_frame.pack(fill="x", pady=10)
        
        def update():
            try:
                new_balance = float(balance_entry.get())
                user = self.storage.get_user(username)
                user.balance = new_balance
                
                new_password = password_entry.get()
                if new_password:
                    if len(new_password) < 4:
                        messagebox.showerror("Error", "Password too short!")
                        return
                    user.password_hash = hashlib.sha256(new_password.encode()).hexdigest()
                
                self.storage.save()
                self._load_users()
                messagebox.showinfo("Success", "✅ User updated!")
                dialog.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid balance!")
        
        tk.Button(btn_frame, text="💾 SAVE CHANGES", command=update,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        
        tk.Button(btn_frame, text="✕ CANCEL", command=dialog.destroy,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)
        
    def _edit_user(self, event):
        """Edit selected user (double-click)"""
        self._edit_selected_user()
        
    def _on_booking_click(self, event):
        """Handle booking click"""
        selection = self.bookings_tree.selection()
        if selection:
            item = self.bookings_tree.item(selection[0])
            table_id = item['values'][0]
            if messagebox.askyesno("Close Booking", f"Close table {table_id}?"):
                self._force_close_table(table_id)
        
    def _show_statistics(self):
        """Show detailed statistics"""
        total_users = len(self.storage.users)
        total_bookings = len(self.storage.bookings)
        total_revenue = sum(b.cost for b in self.storage.bookings.values())
        
        stats = f"""📊 SYSTEM STATISTICS

👥 Total Users: {total_users}
📋 Active Bookings: {total_bookings}
💰 Total Revenue: ${total_revenue:.2f}

🟢 Available Tables: {4 - total_bookings}
🔴 Occupied Tables: {total_bookings}"""
        
        messagebox.showinfo("Statistics", stats)
        
    def _show_booking_stats(self):
        """Show booking statistics"""
        self._show_statistics()
        
    def _force_close_table(self, table_id):
        """Force close a table"""
        if messagebox.askyesno("Confirm", f"Force close Table {table_id}?"):
            if table_id in self.storage.bookings:
                del self.storage.bookings[table_id]
                self.storage.save()
                self._refresh_all()
                messagebox.showinfo("Success", f"✅ Table {table_id} closed")
                
    def _reset_table(self, table_id):
        """Reset table"""
        if table_id in self.storage.bookings:
            if messagebox.askyesno("Confirm", f"Reset Table {table_id}?"):
                del self.storage.bookings[table_id]
                self.storage.save()
                self._refresh_all()
                messagebox.showinfo("Success", f"✅ Table {table_id} reset")
        else:
            messagebox.showinfo("Info", f"Table {table_id} is already empty")
            
    def _clear_all_bookings(self):
        """Clear all bookings"""
        if messagebox.askyesno("⚠️ WARNING", "Clear ALL bookings? This cannot be undone!"):
            self.storage.bookings.clear()
            self.storage.save()
            self._refresh_all()
            messagebox.showinfo("Success", "✅ All bookings cleared")
            
    def _update_rate(self):
        """Update hourly rate"""
        try:
            new_rate = int(self.rate_var.get())
            if new_rate <= 0:
                raise ValueError
                
            global RATE_PER_HOUR
            RATE_PER_HOUR = new_rate
            messagebox.showinfo("Success", f"✅ Rate updated to ${new_rate}/hour")
        except:
            messagebox.showerror("Error", "Please enter a valid positive number")
            
    def _backup_data(self):
        """Backup data to file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_file = f"mahjong_backup_{timestamp}.json"
        
        try:
            shutil.copy2(DATA_FILE, backup_file)
            messagebox.showinfo("Success", f"✅ Data backed up to {backup_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Backup failed: {e}")
            
    def _restore_data(self):
        """Restore data from backup"""
        from tkinter import filedialog
        
        filename = filedialog.askopenfilename(
            title="Select backup file",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                with open(DATA_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    
                self.storage._load()
                self._refresh_all()
                messagebox.showinfo("Success", "✅ Data restored successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Restore failed: {e}")
                
    def _reset_all_data(self):
        """Reset all data"""
        if messagebox.askyesno("⚠️ WARNING", "This will DELETE ALL DATA! Are you sure?"):
            if messagebox.askyesno("⚠️ FINAL WARNING", "This cannot be undone. Continue?"):
                self.storage.users.clear()
                self.storage.bookings.clear()
                self.storage._create_test_data()
                self._refresh_all()
                messagebox.showinfo("Success", "✅ All data has been reset")
                
    def _add_user_dialog(self):
        """Open dialog to add new user"""
        dialog = tk.Toplevel(self)
        dialog.title("Add New User")
        dialog.configure(bg=BG_ROOT)
        dialog.geometry("400x400")
        dialog.resizable(False, False)
        dialog.transient(self)
        dialog.grab_set()
        
        # Center dialog
        dialog.update_idletasks()
        x = (dialog.winfo_screenwidth() - 400) // 2
        y = (dialog.winfo_screenheight() - 400) // 2
        dialog.geometry(f"400x400+{x}+{y}")
        
        # Form
        frame = tk.Frame(dialog, bg=BG_CARD, padx=25, pady=25)
        frame.pack(fill="both", expand=True)
        
        tk.Label(frame, text="➕ ADD NEW USER", font=("Segoe UI", 16, "bold"),
                fg=ACCENT, bg=BG_CARD).pack(pady=(0, 20))
        
        # Username
        tk.Label(frame, text="Username:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        username_entry = tk.Entry(frame, font=("Segoe UI", 12))
        username_entry.pack(fill="x", pady=(0, 15))
        
        # Password
        tk.Label(frame, text="Password:", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        password_entry = tk.Entry(frame, font=("Segoe UI", 12), show="•")
        password_entry.pack(fill="x", pady=(0, 15))
        
        # Balance
        tk.Label(frame, text="Initial Balance ($):", font=("Segoe UI", 11),
                fg=TEXT, bg=BG_CARD).pack(anchor="w", pady=(0, 5))
        balance_entry = tk.Entry(frame, font=("Segoe UI", 12))
        balance_entry.insert(0, "0")
        balance_entry.pack(fill="x", pady=(0, 20))
        
        def add_user():
            username = username_entry.get().strip()
            password = password_entry.get()
            
            try:
                balance = float(balance_entry.get())
            except:
                messagebox.showerror("Error", "Invalid balance amount")
                return
                
            if not username or not password:
                messagebox.showerror("Error", "Please fill all fields")
                return
                
            ok, msg = self.storage.register(username, password)
            if ok:
                user = self.storage.get_user(username)
                if user:
                    user.balance = balance
                    self.storage.save()
                    
                self._load_users()
                messagebox.showinfo("Success", f"✅ User {username} created!")
                dialog.destroy()
            else:
                messagebox.showerror("Error", msg)
                
        # Buttons
        btn_frame = tk.Frame(frame, bg=BG_CARD)
        btn_frame.pack(fill="x", pady=10)
        
        tk.Button(btn_frame, text="✅ CREATE USER", command=add_user,
                 bg=SUCCESS, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="left", padx=5, expand=True)
        
        tk.Button(btn_frame, text="✕ CANCEL", command=dialog.destroy,
                 bg=ERROR, fg="white", font=("Segoe UI", 11, "bold"),
                 padx=20, pady=8, cursor="hand2").pack(side="right", padx=5, expand=True)