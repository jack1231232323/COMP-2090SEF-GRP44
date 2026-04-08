

import hashlib
import datetime

class User:  # Jack
    def __init__(self, username, password_hash, balance=0.0):
        self.username = username
        self.password_hash = password_hash
        self.balance = balance

    def check_password(self, pw):  # Jack
        return self.password_hash == hashlib.sha256(pw.encode()).hexdigest()

class Booking:  
    def __init__(self, table_id, username, hours, start_time, cost):
        self.table_id = table_id
        self.username = username
        self.hours = hours
        self.start_time = start_time
        self.cost = cost

    @property
    def end_time_str(self):  
        start = datetime.datetime.fromisoformat(self.start_time)
        end = start + datetime.timedelta(hours=self.hours)
        return end.strftime("%H:%M")