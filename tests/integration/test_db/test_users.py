import pytest

from api.models.db.user import User
from api.storage.database.users import UsersStorage
from tests.utils import get_random_email


@pytest.mark.asyncio
class TestUsersStorage:
    async def test_count(self, users_storage: UsersStorage):
        assert await users_storage.size() is not None

    async def test_get_users(self, users_storage: UsersStorage):
        users = await users_storage.get_users()

        assert users is not None
        assert isinstance(users, list)
        for user in users:
            assert isinstance(user, User)

    async def test_create_get_users(self, users_storage: UsersStorage):
        initial_users = set(await users_storage.get_users())
        created_users = []
        for _ in range(3):
            user_id = await users_storage.size()
            user = User(
                id=user_id,
                name="irusland",
                age=22,
                about="its me",
                email=get_random_email(),
                password="pasasdasdasdasdasd",
            )
            print(f'>>> {await users_storage.get_users()=}')
            print(f'>>> {user=}')
            print(f'>>> {await users_storage.size()=}')
            created_users.append(await users_storage.create_user(user))

        current_users = set(await users_storage.get_users())

        actual_created_users = current_users.difference(initial_users)
        assert actual_created_users == set(created_users)

    async def test_create_user(self, users_storage: UsersStorage):
        user_id = await users_storage.size()
        assert (
            users_storage.create_user(
                user=User(
                    id=user_id,
                    name="irusland",
                    age=22,
                    about="its me",
                    email=get_random_email(),
                    password="pasasdasdasdasdasd",
                )
            )
            is not None
        )

    async def test_create_and_get_user(self, users_storage: UsersStorage):
        user_id = await users_storage.size()
        user = User(
            id=user_id,
            name="irusland",
            age=22,
            about="its me",
            email=get_random_email(),
            password="pasasdasdasdasdasd",
        )
        await users_storage.create_user(user=user)

        actual_user = await users_storage.get_user(id_=user_id)

        assert actual_user is not None
        assert actual_user.id == user.id
        assert actual_user.name == user.name
        assert actual_user.age == user.age
        assert actual_user.about == user.about
        assert actual_user.email == user.email
        assert actual_user.password == user.password

    async def test_create_user_length_increases(self, users_storage: UsersStorage):
        initial_count = await users_storage.size()
        user = User(
            id=initial_count,
            name="irusland",
            age=22,
            about="its me",
            email=get_random_email(),
            password="pasasdasdasdasdasd",
        )
        await users_storage.create_user(user=user)

        actual_count = await users_storage.size()

        assert actual_count == initial_count + 1

    async def test_create_user_update(self, users_storage: UsersStorage):
        user_id = await users_storage.size()
        user = User(
            id=user_id,
            name="irusland",
            age=22,
            about="its me",
            email=get_random_email(),
            password="pasasdasdasdasdasd",
        )
        new_user = User(
            id=0,
            name="SOME DRASTIC CHANGE",
            age=100,
            about="its definitely not me",
            email=get_random_email(),
            password="qwerty",
        )
        await users_storage.create_user(user=user)
        print(f'>>> GET {await users_storage.get_user(id_=user_id)=}')
        assert await users_storage.update_user(id_=user_id, new_user=new_user) is not None
        print(f'>>> GET {await users_storage.get_user(id_=user_id)=}')

        actual_user = await users_storage.get_user(id_=user_id)
        assert actual_user is not None
        assert actual_user.id == user.id
        assert actual_user.name == new_user.name
        assert actual_user.age == new_user.age
        assert actual_user.about == new_user.about
        assert actual_user.email == new_user.email
        assert actual_user.password == new_user.password

    async def test_find_user(self, users_storage: UsersStorage):
        user = User(
            id=await users_storage.size(),
            name="irusland",
            age=22,
            about="its me",
            email=get_random_email(),
            password="pasasdasdasdasdasd",
        )
        await users_storage.create_user(user=user)

        actual_user = await users_storage.find_user(email=user.email)

        assert actual_user is not None
        assert actual_user.id == user.id
        assert actual_user.name == user.name
        assert actual_user.age == user.age
        assert actual_user.about == user.about
        assert actual_user.email == user.email
        assert actual_user.password == user.password

    async def test_on_user_login(self, users_storage: UsersStorage):
        user = User(
            id=await users_storage.size(),
            name="irusland",
            age=22,
            about="its me",
            email=get_random_email(),
            password="pasasdasdasdasdasd",
        )
        await users_storage.create_user(user=user)
        initial_last_login = (await users_storage.get_user(id_=user.id)).last_login
        assert initial_last_login

        await users_storage.on_user_login(user)

        actual_last_login = (await users_storage.get_user(id_=user.id)).last_login
        assert actual_last_login != initial_last_login
