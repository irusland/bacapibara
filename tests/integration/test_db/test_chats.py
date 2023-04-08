import pytest

from api.app import DatabaseManager
from api.storage.database.chat import ChatStorage


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
