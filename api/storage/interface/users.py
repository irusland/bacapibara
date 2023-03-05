import abc
from abc import ABC

from api.models.db.user import User


class IUsersStorage(ABC):
    @abc.abstractmethod
    def __len__(self) -> int:
        pass

    @abc.abstractmethod
    def create_user(self, user: User) -> User:
        pass

    @abc.abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abc.abstractmethod
    def get_user(self, id_: int) -> User:
        pass

    @abc.abstractmethod
    def update_user(self, id_: int, new_user: User) -> User:
        pass

    @abc.abstractmethod
    def find_user(self, email: str) -> User:
        pass
