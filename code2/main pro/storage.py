import json, os, hashlib
from datetime import datetime
from models import User, Booking
from config import datafile, rateperhour

class Storage:
    def __init__(self):
        self.users = {}
        self.bookings = {}
        self.rate = rateperhour
        self._load()

    def _load(self):
        if not os.path.exists(datafile):
            self._make_test()
            return
        try:
            with open(datafile, 'r', encoding='utf-8') as f:
                raw = json.load(f)
            for uinfo in raw.get('users', {}).values():
                nm = uinfo['username']
                self.users[nm] = User(nm, uinfo['password_hash'], uinfo['balance'])
            for tid, bd in raw.get('bookings', {}).items():
                self.bookings[tid] = Booking(bd['table_id'], bd['username'], bd['hours'], bd['start_time'], bd['cost'])
            self.rate = raw.get('rate', rateperhour)
        except:
            self._make_test()

    def _make_test(self):
        self.users['admin'] = User('admin', hashlib.sha256(b'admin123').hexdigest(), 999999.0)
        self.users['test'] = User('test', hashlib.sha256(b'test123').hexdigest(), 200.0)
        self.users['demo'] = User('demo', hashlib.sha256(b'demo123').hexdigest(), 150.0)
        self.save()

    def save(self):
        out = {
            'users': {u: {'username': v.username, 'password_hash': v.password_hash, 'balance': v.balance} for u,v in self.users.items()},
            'bookings': {tid: {'table_id': b.table_id, 'username': b.username, 'hours': b.hours, 'start_time': b.start_time, 'cost': b.cost} for tid,b in self.bookings.items()},
            'rate': self.rate
        }
        with open(datafile, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2)

    def register(self, uname, pw):
        if uname in self.users:
            return False, "Username exists"
        if len(uname) < 2:
            return False, "Username too short"
        if len(pw) < 4:
            return False, "Password too short"
        self.users[uname] = User(uname, hashlib.sha256(pw.encode()).hexdigest(), 0.0)
        self.save()
        return True, "Registered"

    def login(self, uname, pw):
        u = self.users.get(uname)
        if not u:
            return False, "No such user"
        if not u.check_pw(pw):
            return False, "Wrong password"
        return True, "OK"

    def top_up(self, uname, amt):
        if amt <= 0:
            return False, "Amount must be >0"
        u = self.users.get(uname)
        if not u:
            return False, "User not found"
        u.balance += amt
        self.save()
        return True, "Added $%.2f, new balance $%.2f" % (amt, u.balance)

    def get_user(self, uname):
        return self.users.get(uname)

    def open_table(self, tid, uname, hrs):
        if tid in self.bookings:
            return False, "Table %s occupied" % tid
        if len(self.bookings) >= 4:
            return False, "No free tables"
        cost = hrs * self.rate
        u = self.users.get(uname)
        if not u:
            return False, "User missing"
        if u.balance < cost:
            return False, "Need $%.2f, have $%.2f" % (cost, u.balance)
        u.balance -= cost
        self.bookings[tid] = Booking(tid, uname, hrs, datetime.now().isoformat(), cost)
        self.save()
        return True, "Opened, deducted $%.2f" % cost

    def close_table(self, tid, uname):
        if tid not in self.bookings:
            return False, "Table %s not open" % tid
        b = self.bookings[tid]
        if b.username != uname:
            return False, "Not your table"
        del self.bookings[tid]
        self.save()
        return True, "Table %s closed" % tid

    def get_booking(self, tid):
        return self.bookings.get(tid)

    def get_all_bookings(self):
        return self.bookings.copy()

    def get_user_bookings(self, uname):
        return [b for b in self.bookings.values() if b.username == uname]

    def get_available_tables(self):
        from config import tableids
        return [tid for tid in tableids if tid not in self.bookings]

    def get_occupied_tables(self):
        return list(self.bookings.keys())

    def calc_cost(self, hrs):
        return hrs * self.rate

    def clear_all(self):
        self.users.clear()
        self.bookings.clear()
        if os.path.exists(datafile):
            os.remove(datafile)
        self._make_test()