from datetime import datetime
from typing import Any

from sqlalchemy import Index, select, update
from sqlalchemy.orm import mapped_column, Mapped
from sqlalchemy.sql.functions import func

from api.app import DatabaseManager
from api.errors import UserNotFoundError
from api.models.db.user import User
from api.storage.database.base import Base
from api.storage.interface.users import IUsersStorage


class Users(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    age: Mapped[int] = mapped_column(nullable=False)
    about: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    last_login: Mapped[datetime] = mapped_column(
        nullable=False, server_default=func.now()
    )
    __table_args__ = (
        Index(
            "last_login_id_name_index",
            "last_login",
            "id",
            "name",
            postgresql_ops={"name": "DESC"},
        ),
    )


class UsersStorage(IUsersStorage):
    def __init__(self, database_manager: DatabaseManager):
        self._database_manager = database_manager

    async def size(self) -> int:
        async with self._database_manager.async_session() as session:
            length = await session.execute(func.max(Users.id))
            result = length.scalar()
            if result is None:
                return 0
            return result + 1

    async def create_user(self, user: User) -> User:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                session.add(
                    Users(
                        id=user.id,
                        name=user.name,
                        age=user.age,
                        about=user.about,
                        email=user.email,
                        password=user.password,
                    )
                )

        return user

    async def get_users(self) -> list[User]:
        users = []
        async with self._database_manager.async_session() as session:
            db_users = (await session.execute(select(Users))).all()
            for db_user in db_users:
                db_user = db_user.Users
                users.append(
                    User(
                        id=db_user.id,
                        name=db_user.name,
                        age=db_user.age,
                        about=db_user.about,
                        email=db_user.email,
                        password=db_user.password,
                    )
                )
        return users

    async def _select_user(self, where_clause: Any) -> User:
        async with self._database_manager.async_session() as session:
            db_user = (
                await session.execute(select(Users).where(where_clause))
            ).fetchone()
            if not db_user:
                raise UserNotFoundError(f"User was not found")
            db_user = db_user.Users
            return User(
                id=db_user.id,
                name=db_user.name,
                age=db_user.age,
                about=db_user.about,
                email=db_user.email,
                password=db_user.password,
                last_login=db_user.last_login,
            )

    async def get_user(self, id_: int) -> User:
        return await self._select_user(where_clause=Users.id == id_)

    async def update_user(self, id_: int, new_user: User) -> User:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                await session.execute(
                    update(Users)
                    .where(Users.id == id_)
                    .values(
                        {
                            "name": new_user.name,
                            "age": new_user.age,
                            "about": new_user.about,
                            "email": new_user.email,
                            "password": new_user.password,
                        },
                    )
                )

        return new_user

    async def find_user(self, email: str) -> User:
        return await self._select_user(
            where_clause=Users.email == email,
        )

    async def on_user_login(self, user: User) -> None:
        async with self._database_manager.async_session() as session:
            async with session.begin():
                await session.execute(
                    update(Users)
                    .where(Users.id == user.id)
                    .values({"last_login": datetime.now()})
                )
