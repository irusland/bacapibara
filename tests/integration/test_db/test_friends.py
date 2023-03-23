import random

import pytest

from api.storage.database.friends import FriendsStorage
from api.storage.database.settings import PostgresSettings


@pytest.fixture
def friends_storage(postgres_settings: PostgresSettings) -> FriendsStorage:
    friends_storage = FriendsStorage(postgres_settings=postgres_settings)
    yield friends_storage


class TestFriendsStorage:
    def test_count(self, friends_storage: FriendsStorage):
        assert len(friends_storage) is not None

    def test_get_friends(self, friends_storage: FriendsStorage):
        friends = friends_storage.get_friends()

        assert isinstance(friends, set)
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2

    def test_get_friends_for(self, friends_storage: FriendsStorage):
        friends = friends_storage.get_friends_for(id=0)

        assert isinstance(friends, list)

    def test_add_friend(self, friends_storage: FriendsStorage):
        user_id = random.randint(1, 13337)
        friend_id = random.randint(1, 13337)
        friends = friends_storage.add_friend(id_=user_id, x=friend_id)

        assert isinstance(friends, set)
        assert friends
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2

    def test_add_get_friend(self, friends_storage: FriendsStorage):
        user_id = random.randint(1, 13337)
        friend_id = random.randint(1, 13337)
        friends_storage.add_friend(id_=user_id, x=friend_id)

        friends = friends_storage.get_friends_for(id=user_id)

        assert friends
        assert friend_id in friends

    def test_add_get_all(self, friends_storage: FriendsStorage):
        user_id = random.randint(1, 13337)
        friend_id = random.randint(1, 13337)
        friends_storage.add_friend(id_=user_id, x=friend_id)

        friends = friends_storage.get_friends()

        assert friends
        for pair in friends:
            assert isinstance(pair, tuple)
            assert len(pair) == 2
        assert (user_id, friend_id) in friends
        assert (friend_id, user_id) in friends

    def test_add_len_friend(self, friends_storage: FriendsStorage):
        user_id = random.randint(1, 13337)
        friend_id = random.randint(1, 13337)
        initial_len = len(friends_storage)

        friends_storage.add_friend(id_=user_id, x=friend_id)

        actual_len = len(friends_storage)

        assert actual_len == initial_len + 2
