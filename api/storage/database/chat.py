from sqlalchemy import UniqueConstraint, func

from sqlalchemy import UniqueConstraint
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import selectinload

from api.app import DatabaseManager
from api.models.api.chat import Chat
from api.storage.database.base import Base
from api.storage.interface.chat import IChatStorage


class Chats(Base):
    chat_id: Mapped[int] = mapped_column(nullable=False)
    user_id: Mapped[int] = mapped_column(nullable=False)
    __table_args__ = (UniqueConstraint(chat_id, user_id),)


class ChatStorage(IChatStorage):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def size(self) -> int:
        async with self._database_manager.async_session() as session:
            return await self._get_size(session)

    async def create_chat(self, user_ids: list[int]) -> Chat:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                max_chat_id = await self._get_size(session)
                chat_id = max_chat_id + 1
                session.add_all(
                    [Chats(chat_id=chat_id, user_id=user_id) for user_id in user_ids]
                )

            return Chat(
                chat_id=chat_id,
                user_ids=user_ids,
            )

    async def get_chat(self, chat_id: int) -> Chat:
        async with self._database_manager.async_session() as session:
            result = await session.execute(
                select(Chats.user_id).where(Chats.chat_id == chat_id)
            )
            user_ids = result.scalars().all()
            return Chat(
                chat_id=chat_id,
                user_ids=[user_id for user_id in user_ids],
            )

    async def _get_size(self, session: Session) -> int:
        length = await session.execute(func.max(Chats.chat_id))
        return length.scalar() or 0
