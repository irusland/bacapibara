from sqlalchemy import UniqueConstraint
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import Mapped, Session
from sqlalchemy.orm import mapped_column

from api.storage.database.manager import DatabaseManager
from api.models.api.chat import Chat
from api.storage.database.base import Base
from api.storage.database.messages import Messages
from api.storage.interface.chat import IChatStorage
from api.storage.message import Message


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
                messages=[],
            )

    async def get_chat(self, chat_id: int) -> Chat:
        async with self._database_manager.async_session() as session:
            result = await session.execute(
                select(Chats.user_id).where(Chats.chat_id == chat_id)
            )
            user_ids = result.scalars().all()
            result = await session.execute(
                select(Messages.user_id, Messages.text).where(
                    Messages.chat_id == chat_id
                ).order_by(Messages.id)
            )
            messages = result.all()
            return Chat(
                chat_id=chat_id,
                user_ids=[user_id for user_id in user_ids],
                messages=[
                    Message(
                        user_id=message.user_id,
                        text=message.text,
                    )
                    for message in messages
                ],
            )

    async def _get_size(self, session: Session) -> int:
        length = await session.execute(func.max(Chats.chat_id))
        result = length.scalar()
        if result is None:
            return 0
        return result + 1

    async def add_message(self, chat_id: int, message: Message) -> None:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                session.add(
                    Messages(
                        chat_id=chat_id,
                        user_id=message.user_id,
                        text=message.text,
                    )
                )
