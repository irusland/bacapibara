import dataclasses
from datetime import datetime
from typing import Optional


@dataclasses.dataclass(frozen=True)
class User:
    id: int
    name: str
    age: int
    about: str
    email: str
    password: str
    last_login: Optional[datetime] = None
