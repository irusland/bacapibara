import pytest

from api.storage.database.manager import DatabaseManager
from api.storage.database.chat import ChatStorage
from api.storage.message import Message


@pytest.fixture
def chat_storage(database_manager: DatabaseManager) -> ChatStorage:
    chat_storage = ChatStorage(database_manager=database_manager)
    yield chat_storage


@pytest.mark.asyncio
class TestChatStorage:
    async def test_size(self, chat_storage: ChatStorage):
        assert await chat_storage.size() is not None

    async def test_create(self, chat_storage: ChatStorage):
        max_chat_id = await chat_storage.size()
        user_ids = [1, 2, 4]

        chat = await chat_storage.create_chat(user_ids=user_ids)

        assert chat.chat_id == max_chat_id + 1
        assert chat.user_ids == user_ids

    async def test_create_get(self, chat_storage: ChatStorage):
        max_chat_id = await chat_storage.size()
        user_ids = [1, 2]
        await chat_storage.create_chat(user_ids=user_ids)

        actual_chat = await chat_storage.get_chat(max_chat_id + 1)

        assert actual_chat.chat_id == max_chat_id + 1
        assert actual_chat.user_ids == user_ids

    async def test_add_message(self, chat_storage: ChatStorage):
        user_ids = [1, 2, 4]
        messages = []
        chat = await chat_storage.create_chat(user_ids=user_ids)

        for user_id in user_ids:
            message = Message(user_id=user_id, text=f"a text by {user_id}")
            messages.append(message)
            await chat_storage.add_message(chat_id=chat.chat_id, message=message)

        actual_chat = await chat_storage.get_chat(chat_id=chat.chat_id)
        assert actual_chat.chat_id == chat.chat_id
        assert actual_chat.messages == messages
