from datetime import datetime
import hashlib
import json
import os
from typing import Optional
from models import User, Booking
from config import DATA_FILE, RATE_PER_HOUR

class Storage:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.bookings: dict[str, Booking] = {}
        print("Initializing Storage...")
        self.do_load()
        print(f"Loaded {len(self.users)} users")

    def do_load(self):
        if not os.path.exists(DATA_FILE):
            print(f"Data file {DATA_FILE} does not exist, creating test data")
            self.make_test()
            return
        
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                raw = json.load(f)
                print(f"Loaded data: {raw}")
            
            ud = raw.get("users", {})
            for u in ud.values():
                print(f"Loading user: {u}")
                self.users[u["username"]] = User(**u)
            
            bd = raw.get("bookings", {})
            for tid, b in bd.items():
                print(f"Loading booking: {tid} -> {b}")
                self.bookings[tid] = Booking(**b)
                
            print(f"Successfully loaded {len(self.users)} users, {len(self.bookings)} bookings")
                
        except Exception as e:
            print(f"Error loading data: {e}")
            self.make_test()

    def make_test(self):
        print("Creating test data...")
        
        tu = User(
            username="test",
            password_hash=hashlib.sha256("test123".encode()).hexdigest(),
            balance=200.0
        )
        self.users["test"] = tu
        print(f"Created test user: test")
        
        du = User(
            username="demo",
            password_hash=hashlib.sha256("demo123".encode()).hexdigest(),
            balance=150.0
        )
        self.users["demo"] = du
        print(f"Created test user: demo")
        
        au = User(
            username="admin",
            password_hash=hashlib.sha256("admin123".encode()).hexdigest(),
            balance=999999.0
        )
        self.users["admin"] = au
        print(f"Created admin user: admin")
        
        self.save()
        print("Test data saved")

    def save(self):
        print("Saving data...")
        
        data = {
            "users": {
                k: {
                    "username": v.username,
                    "password_hash": v.password_hash,
                    "balance": v.balance
                } for k, v in self.users.items()
            },
            "bookings": {k: {
                "table_id": v.table_id,
                "username": v.username,
                "hours": v.hours,
                "start_time": v.start_time,
                "cost": v.cost
            } for k, v in self.bookings.items()},
        }
        
        print(f"Saving data: {data}")
        
        os.makedirs(os.path.dirname(DATA_FILE) if os.path.dirname(DATA_FILE) else '.', exist_ok=True)
        
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        print("Data saved")

    def register(self, username: str, password: str) -> tuple[bool, str]:
        print(f"Attempting to register user: {username}")
        
        if username in self.users:
            print(f"Registration failed: Username {username} already exists")
            return False, "Username already exists"
        
        if len(username) < 2:
            print(f"Registration failed: Username too short")
            return False, "Username must be at least 2 characters"
        
        if len(password) < 4:
            print(f"Registration failed: Password too short")
            return False, "Password must be at least 4 characters"
        
        self.users[username] = User(
            username=username,
            password_hash=hashlib.sha256(password.encode()).hexdigest(),
            balance=0.0
        )
        print(f"User {username} registered successfully")
        
        self.save()
        
        if username in self.users:
            print(f"Verification: User {username} exists in memory")
        else:
            print(f"Warning: User {username} not in memory!")
        
        return True, "Registration successful"

    def login(self, username: str, password: str) -> tuple[bool, str]:
        print(f"Login attempt: {username}")
        print(f"Current users in memory: {list(self.users.keys())}")
        
        u = self.users.get(username)
        if not u:
            print(f"Login failed: User {username} does not exist")
            return False, "User does not exist"
        
        if not u.check_password(password):
            print(f"Login failed: Incorrect password")
            return False, "Incorrect password"
        
        print(f"User {username} login successful")
        return True, "Login successful"

    def top_up(self, username: str, amount: float) -> tuple[bool, str]:
        print(f"Top up attempt: {username} +{amount}")
        
        if amount <= 0:
            return False, "Amount must be greater than 0"
        
        u = self.users.get(username)
        if not u:
            print(f"Top up failed: User {username} does not exist")
            return False, "User does not exist"
        
        old = u.balance
        u.balance += amount
        print(f"Top up successful: {old} -> {u.balance}")
        
        self.save()
        return True, f"Top up successful, current balance: ${u.balance:.2f}"

    def get_user(self, username: str) -> Optional[User]:
        u = self.users.get(username)
        print(f"Get user {username}: {'Found' if u else 'Not found'}")
        return u

    def open_table(self, tid: str, username: str, hours: int) -> tuple[bool, str]:
        print(f"Attempting to open table: Table {tid}, User {username}, Hours {hours}")
        
        if tid in self.bookings:
            return False, f"Table {tid} is already occupied"
        
        if len(self.bookings) >= 4:
            return False, "No tables available"
        
        cost = hours * RATE_PER_HOUR
        
        u = self.users.get(username)
        if not u:
            return False, "User does not exist"
        
        if u.balance < cost:
            return False, f"Insufficient balance (need ${cost:.2f})"
        
        u.balance -= cost
        
        self.bookings[tid] = Booking(
            table_id=tid,
            username=username,
            hours=hours,
            start_time=datetime.now().isoformat(),
            cost=cost
        )
        
        print(f"Table opened successfully: Table {tid}, Cost ${cost:.2f}")
        self.save()
        return True, f"Table opened successfully, deducted ${cost:.2f}"

    def close_table(self, tid: str, username: str) -> tuple[bool, str]:
        print(f"Attempting to close table: Table {tid}, User {username}")
        
        if tid not in self.bookings:
            return False, f"Table {tid} is not open"
        
        b = self.bookings[tid]
        if b.username != username:
            return False, "Not authorized to close this table"
        
        del self.bookings[tid]
        print(f"Table closed successfully: Table {tid}")
        
        self.save()
        return True, f"Table {tid} closed"

    def get_booking(self, tid: str) -> Optional[Booking]:
        return self.bookings.get(tid)

    def get_all_bookings(self) -> dict:
        return self.bookings.copy()

    def get_user_bookings(self, username: str) -> list[Booking]:
        return [b for b in self.bookings.values() if b.username == username]

    def get_available_tables(self) -> list[str]:
        from config import TABLE_IDS
        return [tid for tid in TABLE_IDS if tid not in self.bookings]

    def get_occupied_tables(self) -> list[str]:
        return list(self.bookings.keys())

    def calc_cost(self, hours: int) -> float:
        return hours * RATE_PER_HOUR

    def clear_all(self):
        self.users.clear()
        self.bookings.clear()
        if os.path.exists(DATA_FILE):
            os.remove(DATA_FILE)
        self.make_test()