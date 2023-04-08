from sqlalchemy import UniqueConstraint, ForeignKey, func, select
from sqlalchemy.orm import Mapped, mapped_column

from api.storage.database.manager import DatabaseManager
from api.storage.database.base import Base
from api.storage.interface.friends import IFriendsStorage


class Friends(Base):
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    friend_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    __table_args__ = (UniqueConstraint(user_id, friend_id),)


class FriendsStorage(IFriendsStorage):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def size(self) -> int:
        async with self._database_manager.async_session() as session:
            return (await session.execute(select(func.count(Friends.id)))).scalar_one()

    async def add_friend(self, id_: int, x: int) -> set[tuple[int, int]]:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                session.add_all(
                    [
                        Friends(user_id=id_, friend_id=x),
                        Friends(user_id=x, friend_id=id_),
                    ]
                )

        return await self.get_friends()

    async def get_friends(self) -> set[tuple[int, int]]:
        async with self._database_manager.async_session() as session:
            db_friends = (await session.execute(select(Friends))).all()
            friends = set()
            for db_friend in db_friends:
                db_friendship = db_friend.Friends
                pair = (db_friendship.user_id, db_friendship.friend_id)
                friends.add(pair)
            return friends

    async def get_friends_for(self, id: int) -> list[int]:
        async with self._database_manager.async_session() as session:
            result = await session.execute(
                select(Friends.friend_id).where(Friends.user_id == id)
            )

            return result.scalars().all()
