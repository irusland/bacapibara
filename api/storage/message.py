from pydantic import BaseModel


class Message(BaseModel):
    user_id: int
    text: str

    def __str__(self):
        return f"({self.user_id}): {self.text}"
