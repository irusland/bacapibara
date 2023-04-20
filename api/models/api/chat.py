from pydantic import BaseModel

from api.storage.message import Message


class Chat(BaseModel):
    chat_id: int
    user_ids: list[int]
    messages: list[Message]
