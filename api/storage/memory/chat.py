from api.models.api.chat import Chat
from api.storage.interface.chat import IChatStorage


class ChatStorage(IChatStorage):
    def __init__(self):
        self._chats: dict[int, Chat] = {}

    def __len__(self) -> int:
        return len(self._chats)

    def create_chat(self, user_ids: list[int]) -> Chat:
        next_chat_id = len(self._chats)
        new_chat = Chat(chat_id=next_chat_id, user_ids=user_ids)
        self._chats[new_chat.chat_id] = new_chat
        return new_chat

    def get_chat(self, chat_id: int) -> Chat:
        return self._chats[chat_id]
