import psycopg2
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr

from api.storage.database.settings import PostgresSettings

from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base, as_declarative


@as_declarative()
class Base(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()
    id: Mapped[int] = mapped_column(primary_key=True)


class BaseStorage:
    def __init__(self, table_name: str, postgres_settings: PostgresSettings):
        self._table_name = table_name
        self._connection = None
        self._connection = psycopg2.connect(
            host=postgres_settings.host,
            database=postgres_settings.db,
            user=postgres_settings.user,
            password=postgres_settings.password,
        )

    def __del__(self):
        if self._connection is not None:
            self._connection.close()

    def __len__(self) -> int:
        with self._connection:
            with self._connection.cursor() as cursor:
                cursor.execute(f"SELECT COUNT(*) FROM {self._table_name}")
                (len_,) = cursor.fetchone()
        return len_
