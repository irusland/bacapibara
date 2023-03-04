import dataclasses


@dataclasses.dataclass
class User:
    id: int
    name: str
    age: int
    about: str
    email: str
    password: str
