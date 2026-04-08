import hashlib
import datetime

class User:
    def __init__(self, username, pw_hash, balance=0.0):
        self.username = username
        self.password_hash = pw_hash
        self.balance = balance

    def check_pw(self, plain):
        return self.password_hash == hashlib.sha256(plain.encode()).hexdigest()


class Booking:
    def __init__(self, tid, uname, hrs, start, cost):
        self.table_id = tid
        self.username = uname
        self.hours = hrs
        self.start_time = start
        self.cost = cost

    @property
    def end_time_str(self):
        st = datetime.datetime.fromisoformat(self.start_time)
        et = st + datetime.timedelta(hours=self.hours)
        return et.strftime("%H:%M")