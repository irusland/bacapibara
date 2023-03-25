import random

import pytest
import pytest_asyncio

from api.storage.database.manager import DatabaseManager
from api.models.db.user import User
from api.storage.database.friends import FriendsStorage
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage
from tests.utils import get_random_email


@pytest.fixture
def friends_storage(
    postgres_settings: PostgresSettings,
    users_storage: UsersStorage,
    database_manager: DatabaseManager,
) -> FriendsStorage:
    friends_storage = FriendsStorage(database_manager=database_manager)
    yield friends_storage


async def create_user(users_storage: UsersStorage) -> User:
    user_id = await users_storage.size()
    user = User(
        id=user_id,
        name="irusland",
        age=22,
        about="its me",
        email=get_random_email(),
        password="pasasdasdasdasdasd",
    )
    return await users_storage.create_user(user=user)


@pytest_asyncio.fixture
async def user_1(users_storage: UsersStorage) -> User:
    return await create_user(users_storage=users_storage)


@pytest_asyncio.fixture
async def user_2(users_storage: UsersStorage) -> User:
    return await create_user(users_storage=users_storage)


@pytest.mark.asyncio
class TestFriendsStorage:
    async def test_count(self, friends_storage: FriendsStorage):
        assert await friends_storage.size() is not None

    async def test_get_friends(self, friends_storage: FriendsStorage):
        friends = await friends_storage.get_friends()

        assert isinstance(friends, set)
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2

    async def test_get_friends_for(self, friends_storage: FriendsStorage):
        friends = await friends_storage.get_friends_for(id=0)

        assert isinstance(friends, list)

    async def test_add_friend(
        self, friends_storage: FriendsStorage, user_1: User, user_2: User
    ):
        user_id = user_1.id
        friend_id = user_2.id
        friends = await friends_storage.add_friend(id_=user_id, x=friend_id)

        assert isinstance(friends, set)
        assert friends
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2

    async def test_add_get_friend(
        self, friends_storage: FriendsStorage, user_1: User, user_2: User
    ):
        user_id = user_1.id
        friend_id = user_2.id
        await friends_storage.add_friend(id_=user_id, x=friend_id)

        friends = await friends_storage.get_friends_for(id=user_id)

        assert friends
        assert friend_id in friends

    async def test_add_get_all(
        self, friends_storage: FriendsStorage, user_1: User, user_2: User
    ):
        user_id = user_1.id
        friend_id = user_2.id
        await friends_storage.add_friend(id_=user_id, x=friend_id)

        friends = await friends_storage.get_friends()

        assert friends
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2
        assert (user_id, friend_id) in friends
        assert (friend_id, user_id) in friends

    async def test_add_len_friend(
        self, friends_storage: FriendsStorage, user_1: User, user_2: User
    ):
        user_id = user_1.id
        friend_id = user_2.id
        initial_len = await friends_storage.size()

        print(f">>> {await friends_storage.get_friends_for(id=0)=}")

        added = await friends_storage.add_friend(id_=user_id, x=friend_id)
        print(f">>> {added=}")

        actual_len = await friends_storage.size()
        print(f">>> {await friends_storage.get_friends_for(id=0)=}")
        print(f">>> {await friends_storage.get_friends()=}")

        assert actual_len == initial_len + 2
