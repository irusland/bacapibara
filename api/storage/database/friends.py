from api.storage.database.base import BaseStorage
from api.storage.database.settings import PostgresSettings
from api.storage.interface.friends import IFriendsStorage


class FriendsStorage(BaseStorage, IFriendsStorage):
    def __init__(self, postgres_settings: PostgresSettings):
        super().__init__(table_name="friends", postgres_settings=postgres_settings)
        self._init_db()

    def _init_db(self):
        create_if_not_exists_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            id SERIAL NOT NULL PRIMARY KEY,
            user_id integer NOT NULL,
            friend_id integer NOT NULL,
            UNIQUE (user_id, friend_id),
            CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users (id),
            CONSTRAINT fk_friend_id FOREIGN KEY (friend_id) REFERENCES users (id)
        );
        """
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(create_if_not_exists_table_query)

    def add_friend(self, id_: int, x: int) -> set[tuple[int, int]]:
        with self._connection:
            with self._connection.cursor() as cursor:
                insertion_query = f"""
                    INSERT INTO {self._table_name} (user_id, friend_id)
                    VALUES (%(user_id)s, %(friend_id)s);
                    """
                cursor.execute(
                    insertion_query,
                    {"user_id": id_, "friend_id": x},
                )
                cursor.execute(
                    insertion_query,
                    {"user_id": x, "friend_id": id_},
                )
        return self.get_friends()

    def get_friends(self) -> set[tuple[int, int]]:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT user_id, friend_id FROM {self._table_name};
                    """,
                )
                return set(cursor.fetchall())

    def get_friends_for(self, id: int) -> list[int]:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT friend_id FROM {self._table_name}
                    WHERE user_id = %(user_id)s;
                    """,
                    {"user_id": id},
                )
                return list(pair[0] for pair in cursor.fetchall())
