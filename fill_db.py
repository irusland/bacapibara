import asyncio
import logging
import random
from uuid import uuid4

import faker as faker
import tqdm as tqdm
from sqlalchemy import select, func

from api.storage.database.manager import DatabaseManager
from api.models.db.user import User
from api.storage.database.friends import FriendsStorage
from api.storage.database.messages import Messages
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage, Users

import logging

logging.disable(logging.INFO)


fake = faker.Faker(locale="ru_RU")

postgres_settings = PostgresSettings()
database_manager = DatabaseManager(postgres_settings=postgres_settings)
users_storage = UsersStorage(database_manager=database_manager)
friends_storage = FriendsStorage(database_manager=database_manager)

batch_size = 1000
batch_count = 1000


async def _create_users(users_storage: UsersStorage, users_to_create: list[User]):
    users = [
        Users(
            id=user.id,
            name=user.name,
            age=user.age,
            about=user.about,
            email=user.email,
            password=user.password,
        )
        for user in users_to_create
    ]
    async with database_manager.async_session() as session:
        async with session.begin():
            session.add_all(users)


async def create_users():
    current_user_id = await users_storage.size()
    if current_user_id >= batch_count * batch_size:
        return
    for c in tqdm.trange(batch_count):
        users_to_create = []
        for b in range(batch_size):
            user = User(
                id=current_user_id,
                name=fake.name(),
                age=fake.pyint(min_value=1, max_value=100),
                about=fake.text(max_nb_chars=13),
                email=uuid4().hex + fake.email(),
                password=fake.password(),
            )
            users_to_create.append(user)
            current_user_id += 1
        await _create_users(users_storage, users_to_create)


def _create_friends(
    friends_storage: FriendsStorage, friends_to_create: list[tuple[int, int, int]]
):
    with friends_storage._connection:
        with friends_storage._connection.cursor() as cursor:
            arg_str = ",".join(["%s"] * len(friends_to_create[0]))
            args_str = ",".join(
                (cursor.mogrify(f"({arg_str})", x)).decode() for x in friends_to_create
            )
            cursor.execute(
                f"INSERT INTO {friends_storage._table_name} VALUES " + args_str
            )


async def create_friends():
    current_friends_count = await friends_storage.size()
    if current_friends_count >= batch_count * batch_size:
        return

    current_users_count = users_storage.size()
    current_friends_count += 1
    for c in tqdm.trange(batch_count):
        friends_to_create = []
        for b in range(batch_size):
            user_id = random.randint(0, current_users_count - 1)
            friend_id = random.randint(0, current_users_count - 1)
            if friend_id == user_id:
                continue
            friends_to_create.append((current_friends_count, user_id, friend_id))
            current_friends_count += 1
            friends_to_create.append((current_friends_count, friend_id, user_id))
            current_friends_count += 1
        try:
            _create_friends(friends_storage, friends_to_create)
        except:
            pass


async def create_messages():
    async with database_manager.async_session() as session:
        current_messages_count = (
            await session.execute(select(func.count(Messages.id)))
        ).scalar_one()

    if current_messages_count >= batch_count * batch_size:
        return

    for c in tqdm.trange(batch_count):
        messages_to_create = []
        for b in range(batch_size):
            messages_to_create.append(
                Messages(
                    chat_id=0,
                    user_id=1,
                    text=fake.text(),
                )
            )
            current_messages_count += 1
        async with database_manager.async_session() as session:
            async with session.begin():
                session.add_all(messages_to_create)


asyncio.run(create_users())
# create_friends()

# asyncio.run(create_messages())
