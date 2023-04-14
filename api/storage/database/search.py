from sqlalchemy import select, func, text
from sqlalchemy.dialects.postgresql import to_tsquery

from api.storage.database.manager import DatabaseManager
from api.storage.database.messages import Messages
from api.storage.database.users import Users
from api.storage.interface.search import ISearchStorage


class SearchStorage(ISearchStorage):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def messages_by_text(self, text: str) -> list[Messages]:
        async with self._database_manager.async_session() as session:
            ts_query = func.to_tsvector("russian", Messages.text).op("@@")(
                to_tsquery("russian", text)
            )
            rows = await session.execute(select(Messages).filter(ts_query).limit(100))
            return [row.Messages for row in rows]

    async def users_by_name(self, name: str) -> list[Users]:
        async with self._database_manager.async_session() as session:
            ts_query = text(
                f"to_tsvector('russian'::regconfig, name || ' ' || about) @@ to_tsquery('russian', '{name}')"
            )
            rows = await session.execute(select(Users).filter(ts_query).limit(100))
            return [row.Users for row in rows]
