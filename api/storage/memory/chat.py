from api.models.api.chat import Chat
from api.storage.interface.chat import IChatStorage
from api.storage.message import Message


class ChatStorage(IChatStorage):
    def __init__(self):
        self._chats: dict[int, Chat] = {}

    async def size(self) -> int:
        return len(self._chats)

    async def create_chat(self, user_ids: list[int]) -> Chat:
        next_chat_id = len(self._chats)
        new_chat = Chat(chat_id=next_chat_id, user_ids=user_ids, messages=[])
        self._chats[new_chat.chat_id] = new_chat
        return new_chat

    async def get_chat(self, chat_id: int) -> Chat:
        return self._chats[chat_id]

    async def add_message(self, chat_id: int, message: Message) -> None:
        self._chats[chat_id].messages.append(message)
