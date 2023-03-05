import random

import pytest

from api.storage.database.chat import ChatStorage
from api.storage.database.settings import PostgresSettings


@pytest.fixture
def chat_storage(postgres_settings: PostgresSettings) -> ChatStorage:
    chat_storage = ChatStorage(postgres_settings=postgres_settings)
    yield chat_storage


class TestChatStorage:
    def test_len(self, chat_storage: ChatStorage):
        assert len(chat_storage) is not None

    def test_create(self, chat_storage: ChatStorage):
        max_chat_id = len(chat_storage)
        user_ids = [1, 2, 4]

        chat = chat_storage.create_chat(user_ids=user_ids)

        assert chat.chat_id == max_chat_id + 1
        assert chat.user_ids == user_ids

    def test_create_get(self, chat_storage: ChatStorage):
        max_chat_id = len(chat_storage)
        user_ids = [1, 2]
        chat_storage.create_chat(user_ids=user_ids)

        actual_chat = chat_storage.get_chat(max_chat_id + 1)

        assert actual_chat.chat_id == max_chat_id + 1
        assert actual_chat.user_ids == user_ids
