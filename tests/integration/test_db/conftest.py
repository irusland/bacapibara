import psycopg2
import pytest

from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage


@pytest.fixture()
def postgres_settings() -> PostgresSettings:
    return PostgresSettings()


@pytest.fixture
def users_storage(postgres_settings: PostgresSettings) -> UsersStorage:
    users_storage = UsersStorage(postgres_settings=postgres_settings)
    yield users_storage

    connection = psycopg2.connect(
        host=postgres_settings.host,
        database=postgres_settings.db,
        user=postgres_settings.user,
        password=postgres_settings.password,
    )

    with connection:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                DELETE FROM friends
                WHERE user_id IN (SELECT id FROM users WHERE email LIKE %(email)s);
                """,
                {
                    "email": "test_%",
                },
            )
            cursor.execute(
                f"""
                DELETE FROM {users_storage._table_name} CASCADE
                WHERE email LIKE %(email)s;
                """,
                {
                    "email": "test_%",
                },
            )
