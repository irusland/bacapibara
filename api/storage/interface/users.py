import abc
from abc import ABC

from api.models.db.user import User


class IUsersStorage(ABC):
    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_user(self, user: User) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_users(self) -> list[User]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_user(self, id_: int) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_user(self, id_: int, new_user: User) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_user(self, email: str) -> User:
        raise NotImplementedError()

    @abc.abstractmethod
    def on_user_login(self, user: User) -> None:
        raise NotImplementedError()
