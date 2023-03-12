import faker as faker

from api.models.db.user import User
from api.storage.database.friends import FriendsStorage
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage

fake = faker.Faker()

postgres_settings = PostgresSettings()
users_storage = UsersStorage(postgres_settings=postgres_settings)
friends_storage = FriendsStorage(postgres_settings=postgres_settings)

batch_size = 1000
batch_count = 1000


current_user_id = len(users_storage)
for c in range(batch_count):
    users_to_create=[]
    for b in range(batch_size):
        user = User(
            id=current_user_id,
            name=fake.name(),
            age=fake.pyint(min_value=1, max_value=100),
            about=fake.text(),
            email=fake.email(),
            password=fake.password(),
        )
        users_to_create.append(user)
        current_user_id += 1
    users_storage.create_users(users_to_create)
