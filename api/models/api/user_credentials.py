from pydantic import BaseModel


class UserCredentials(BaseModel):
    id: int
