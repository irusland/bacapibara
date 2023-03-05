import pytest

from api.models.db.user import User
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage


@pytest.fixture
def users_storage(postgres_settings: PostgresSettings) -> UsersStorage:
    return UsersStorage(postgres_settings=postgres_settings)


class TestUsersStorage:
    def test_count(self, users_storage: UsersStorage):
        assert len(users_storage) is not None

    def test_get_users(self, users_storage: UsersStorage):
        users = users_storage.get_users()

        assert users is not None
        assert isinstance(users, list)
        for user in users:
            assert isinstance(user, User)

    def test_create_user(self, users_storage: UsersStorage):
        user_id = len(users_storage)
        assert users_storage.create_user(
            user=User(
                id=user_id,
                name='irusland',
                age=22,
                about='its me',
                email='irusland@mail.ru',
                password='pasasdasdasdasdasd',
            )
        ) is not None

    def test_create_and_get_user(self, users_storage: UsersStorage):
        user_id = len(users_storage)
        user = User(
            id=user_id,
            name='irusland',
            age=22,
            about='its me',
            email='irusland@mail.ru',
            password='pasasdasdasdasdasd',
        )
        users_storage.create_user(
            user=user
        )

        actual_user = users_storage.get_user(id_=user_id)

        assert actual_user is not None
        assert actual_user.id == user.id
        assert actual_user.name == user.name
        assert actual_user.age == user.age
        assert actual_user.about == user.about
        assert actual_user.email == user.email
        assert actual_user.password == user.password

    def test_create_user_length_increases(self, users_storage: UsersStorage):
        initial_count = len(users_storage)
        user = User(
            id=initial_count,
            name='irusland',
            age=22,
            about='its me',
            email='irusland@mail.ru',
            password='pasasdasdasdasdasd',
        )
        users_storage.create_user(
            user=user
        )

        actual_count = len(users_storage)

        assert actual_count == initial_count + 1

    def test_create_user_update(self, users_storage: UsersStorage):
        user_id = len(users_storage)
        user = User(
            id=user_id,
            name='irusland',
            age=22,
            about='its me',
            email='irusland@mail.ru',
            password='pasasdasdasdasdasd',
        )
        new_user = User(
            id=0,
            name='SOME DRASTIC CHANGE',
            age=100,
            about='its definitely not me',
            email='bruh@mail.ru',
            password='qwerty',
        )
        users_storage.create_user(
            user=user
        )

        assert users_storage.update_user(
            id_=user_id,
            new_user=new_user,
        ) is not None

        actual_user = users_storage.get_user(id_=user_id)
        assert actual_user is not None
        assert actual_user.id == user.id
        assert actual_user.name == new_user.name
        assert actual_user.age == new_user.age
        assert actual_user.about == new_user.about
        assert actual_user.email == new_user.email
        assert actual_user.password == new_user.password
