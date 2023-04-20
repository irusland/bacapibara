import faker
import pytest

from api.models.db.user import User
from api.storage.database.manager import DatabaseManager
from api.storage.database.messages import Messages
from api.storage.database.search import SearchStorage
from api.storage.database.users import UsersStorage

fake = faker.Faker(locale="ru_RU")


@pytest.fixture()
def search_storage(database_manager: DatabaseManager) -> SearchStorage:
    return SearchStorage(database_manager=database_manager)


@pytest.mark.asyncio
class TestSearchStorage:
    async def test_search_messages(
        self, database_manager: DatabaseManager, search_storage: SearchStorage
    ):
        text = fake.text()
        word = text.split()[0]
        message = Messages(
            chat_id=0,
            user_id=1,
            text=text,
        )
        async with database_manager.async_session() as session:
            async with session.begin():
                session.add(message)

        actual_messages = await search_storage.messages_by_text(word)

        for actual_text in [message.text for message in actual_messages]:
            if word.lower() in actual_text.lower():
                return
        raise AssertionError("text was not found")

    async def test_search_users(
        self,
        database_manager: DatabaseManager,
        search_storage: SearchStorage,
        users_storage: UsersStorage,
    ):
        name = "Руслан"
        await users_storage.create_user(
            user=User(
                id=await users_storage.size(),
                name=name,
                age=0,
                about="Программист",
                email="ь",
                password="asd",
            )
        )

        actual_users = await search_storage.users_by_name(name=name)

        for actual_name in [user.name for user in actual_users]:
            if name.lower() in actual_name.lower():
                return
        raise AssertionError("user was not found")
