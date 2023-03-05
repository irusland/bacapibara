from typing import Any

from api.errors import UserNotFoundError
from api.models.db.user import User
from api.storage.database.settings import PostgresSettings
from api.storage.interface.users import IUsersStorage
import psycopg2


class UsersStorage(IUsersStorage):
    def __init__(self, postgres_settings: PostgresSettings):
        self._table_name = "users"
        self._connection = None
        self._connection = psycopg2.connect(
            host=postgres_settings.host,
            database=postgres_settings.db,
            user=postgres_settings.user,
            password=postgres_settings.password,
        )
        self._init_db()

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

    def _init_db(self):
        cursor = self._connection.cursor()
        create_if_not_exists_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id integer NOT NULL PRIMARY KEY,
            name varchar(45) NOT NULL,
            age integer NOT NULL,
            about varchar(450) NOT NULL,
            email varchar(45) NOT NULL UNIQUE,
            password varchar(450) NOT NULL
        );
        """
        cursor.execute(create_if_not_exists_table_query)
        self._connection.commit()

        cursor.close()

    def __len__(self) -> int:
        cursor = self._connection.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {self._table_name}")
        (len_,) = cursor.fetchone()
        cursor.close()
        return len_

    def create_user(self, user: User) -> User:
        cursor = self._connection.cursor()
        cursor.execute(
            f"""
            INSERT INTO {self._table_name} (id, name, age, about, email, password)
            VALUES (%(id)s, %(name)s, %(age)s, %(about)s, %(email)s, %(password)s);
            """,
            {
                "id": user.id,
                "name": user.name,
                "age": user.age,
                "about": user.about,
                "email": user.email,
                "password": user.password,
            },
        )
        self._connection.commit()
        cursor.close()
        return user

    def get_users(self) -> list[User]:
        cursor = self._connection.cursor()
        cursor.execute(
            f"""
            SELECT id, name, age, about, email, password FROM {self._table_name}
            """
        )
        raw_users = cursor.fetchmany()
        cursor.close()
        users = []
        for id_, name, age, about, email, password in raw_users:
            users.append(
                User(
                    id=id_,
                    name=name,
                    age=age,
                    about=about,
                    email=email,
                    password=password,
                )
            )
        return users

    def _select_user(self, raw_where_clause: str, data: dict[str, Any]) -> User:
        cursor = self._connection.cursor()
        cursor.execute(
            f"""
            SELECT id, name, age, about, email, password 
            FROM {self._table_name}
            WHERE {raw_where_clause}
            """,
            data,
        )
        id_, name, age, about, email, password = cursor.fetchone()
        user = User(
            id=id_,
            name=name,
            age=age,
            about=about,
            email=email,
            password=password,
        )
        cursor.close()
        return user

    def get_user(self, id_: int) -> User:
        return self._select_user(raw_where_clause="id = %(id)s", data={"id": id_})

    def update_user(self, id_: int, new_user: User) -> User:
        cursor = self._connection.cursor()
        cursor.execute(
            f"""
            UPDATE {self._table_name} 
            SET name = %(name)s,
                age = %(age)s,
                about = %(about)s,
                email = %(email)s,
                password = %(password)s
            WHERE id = %(id)s
            """,
            {
                "id": id_,
                "name": new_user.name,
                "age": new_user.age,
                "about": new_user.about,
                "email": new_user.email,
                "password": new_user.password,
            },
        )
        return new_user

    def find_user(self, email: str) -> User:
        return self._select_user(
            raw_where_clause="email = %(email)s", data={"email": email}
        )
