from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Mapped, mapped_column

from api.models.key_value.announcement import Announcement
from api.storage.database.base import Base
from api.storage.database.manager import DatabaseManager
from api.storage.interface.announcements import IAnnouncementStorage


class Announcements(Base):
    statement: Mapped[str] = mapped_column(nullable=False)
    by: Mapped[int] = mapped_column(nullable=False)
    at: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )


class AnnouncementStorage(IAnnouncementStorage):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def add_announcement(self, user_id: int, announcement: Announcement):
        async with self._database_manager.async_session() as session:
            async with session.begin():
                session.add(Announcements(statement=announcement.statement.content, by=announcement.by, at=announcement.at))

    async def size(self) -> int:
        async with self._database_manager.async_session() as session:
            return (await session.execute(select(func.count(Announcements.id)))).scalar_one()
