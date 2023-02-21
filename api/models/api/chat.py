from pydantic import BaseModel


class Chat(BaseModel):
    chat_id: int
    user_ids: list[int]
