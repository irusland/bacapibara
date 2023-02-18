from uuid import UUID

from pydantic import BaseModel, constr, conint


class NewUser(BaseModel):
    name: str
    age: int
    about: str
    email: str
    password: str
