import dataclasses


@dataclasses.dataclass(frozen=True)
class User:
    id: int
    name: str
    age: int
    about: str
    email: str
    password: str
