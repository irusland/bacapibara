import abc
from abc import ABC

from api.models.db.user import User


class IUsersStorage(ABC):
    @abc.abstractmethod
    async def size(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_user(self, user: User) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_users(self) -> list[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_user(self, id_: int) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    async def update_user(self, id_: int, new_user: User) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    async def find_user(self, email: str) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    async def on_user_login(self, user: User) -> None:
        raise NotImplementedError()
