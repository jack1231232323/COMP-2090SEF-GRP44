from dataclasses import dataclass
import hashlib
import datetime
from typing import Optional

@dataclass
class User:
    username: str
    password_hash: str
    balance: float = 0.0

    def check_password(self, pw: str) -> bool:
        return self.password_hash == hashlib.sha256(pw.encode()).hexdigest()


@dataclass
class Booking:
    table_id: str
    username: str
    hours: int
    start_time: str
    cost: float

    @property
    def end_time_str(self) -> str:
        start = datetime.datetime.fromisoformat(self.start_time)
        end = start + datetime.timedelta(hours=self.hours)
        return end.strftime("%H:%M")