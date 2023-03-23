from api.models.api.chat import Chat
from api.storage.database.base import BaseStorage
from api.storage.database.settings import PostgresSettings
from api.storage.interface.chat import IChatStorage


class ChatStorage(BaseStorage, IChatStorage):
    def __init__(self, postgres_settings: PostgresSettings):
        super().__init__("chats", postgres_settings)
        self._init_db()

    def _init_db(self):
        create_if_not_exists_table_query = f"""
        CREATE TABLE IF NOT EXISTS {self._table_name} (
            chat_id integer NOT NULL,
            user_id integer NOT NULL,
            UNIQUE (chat_id, user_id)
        );
        """
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(create_if_not_exists_table_query)

    def __len__(self) -> int:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT COALESCE(MAX(chat_id), 0) FROM {self._table_name};
                    """
                )
                (max_chat_id,) = cursor.fetchone()
                return max_chat_id

    def create_chat(self, user_ids: list[int]) -> Chat:
        max_chat_id = self.__len__()
        with self._connection:
            with self._connection.cursor() as cursor:
                chat_id = max_chat_id + 1
                chat_insertion_query = f"""
                    INSERT INTO {self._table_name} (chat_id, user_id)
                    VALUES (%(chat_id)s, %(user_id)s);
                    """
                for user_id in user_ids:
                    cursor.execute(
                        chat_insertion_query,
                        {
                            "chat_id": chat_id,
                            "user_id": user_id,
                        },
                    )

                return Chat(
                    chat_id=chat_id,
                    user_ids=user_ids,
                )

    def get_chat(self, chat_id: int) -> Chat:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(
                    f"""
                    SELECT user_id FROM {self._table_name}
                    WHERE chat_id = %(chat_id)s;
                    """,
                    {"chat_id": chat_id},
                )
                return Chat(
                    chat_id=chat_id,
                    user_ids=[user_id for (user_id,) in cursor.fetchall()],
                )
