# storage.py
# Jack's part - core storage and file I/O
# Choi's part - user management (register, login, top-up)
# Guo's part - table operations (open, close, bookings)

import json
import os
import hashlib
from datetime import datetime
from models import User, Booking
from config import DATA_FILE, RATE_PER_HOUR

class Storage:  # Jack overall
    def __init__(self):  # Jack
        self.users = {}
        self.bookings = {}
        self._load_data()

    def _load_data(self):  # Jack
        if not os.path.exists(DATA_FILE):
            self.make_test()
            return
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            for u in raw.get('users', {}).values():
                self.users[u['username']] = User(u['username'], u['password_hash'], u['balance'])
            for tid, b in raw.get('bookings', {}).items():
                self.bookings[tid] = Booking(b['table_id'], b['username'], b['hours'], b['start_time'], b['cost'])
        except Exception as e:
            print(f"Load error: {e}")
            self.make_test()

    def make_test(self):  # Choi
        admin = User('admin', hashlib.sha256('admin123'.encode()).hexdigest(), 999999.0)
        self.users['admin'] = admin
        test = User('test', hashlib.sha256('test123'.encode()).hexdigest(), 200.0)
        self.users['test'] = test
        demo = User('demo', hashlib.sha256('demo123'.encode()).hexdigest(), 150.0)
        self.users['demo'] = demo
        self.save()

    def save(self):  # Jack
        data = {
            'users': {u: {'username': v.username, 'password_hash': v.password_hash, 'balance': v.balance}
                      for u, v in self.users.items()},
            'bookings': {tid: {'table_id': b.table_id, 'username': b.username,
                               'hours': b.hours, 'start_time': b.start_time, 'cost': b.cost}
                         for tid, b in self.bookings.items()}
        }
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # Choi's user methods
    def register(self, username, password):
        if username in self.users:
            return False, "Username already exists"
        if len(username) < 2:
            return False, "Username must be at least 2 characters"
        if len(password) < 4:
            return False, "Password must be at least 4 characters"
        self.users[username] = User(username, hashlib.sha256(password.encode()).hexdigest(), 0.0)
        self.save()
        return True, "Registration successful"

    def login(self, username, password):
        user = self.users.get(username)
        if not user:
            return False, "User does not exist"
        if not user.check_password(password):
            return False, "Incorrect password"
        return True, "Login successful"

    def top_up(self, username, amount):
        if amount <= 0:
            return False, "Amount must be positive"
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        user.balance += amount
        self.save()
        return True, f"Top up successful. New balance: ${user.balance:.2f}"

    def get_user(self, username):
        return self.users.get(username)

    # Guo's table methods
    def open_table(self, tid, username, hours):
        if tid in self.bookings:
            return False, f"Table {tid} is already occupied"
        if len(self.bookings) >= 4:
            return False, "No available tables"
        cost = hours * RATE_PER_HOUR
        user = self.users.get(username)
        if not user:
            return False, "User not found"
        if user.balance < cost:
            return False, f"Insufficient balance (need ${cost:.2f})"
        user.balance -= cost
        self.bookings[tid] = Booking(tid, username, hours, datetime.now().isoformat(), cost)
        self.save()
        return True, f"Table opened, deducted ${cost:.2f}"

    def close_table(self, tid, username):
        if tid not in self.bookings:
            return False, f"Table {tid} is not open"
        booking = self.bookings[tid]
        if booking.username != username:
            return False, "Not authorized to close this table"
        del self.bookings[tid]
        self.save()
        return True, f"Table {tid} closed"

    def get_booking(self, tid):
        return self.bookings.get(tid)

    def get_all_bookings(self):
        return self.bookings.copy()

    def get_user_bookings(self, username):
        return [b for b in self.bookings.values() if b.username == username]

    def get_available_tables(self):
        from config import TABLE_IDS
        return [tid for tid in TABLE_IDS if tid not in self.bookings]

    def get_occupied_tables(self):
        return list(self.bookings.keys())

    def calc_cost(self, hours):
        return hours * RATE_PER_HOUR

    def clear_all(self):  # Jack
        self.users.clear()
        self.bookings.clear()
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        self.make_test()