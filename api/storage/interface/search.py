import abc
from abc import ABC

from api.models.db.user import User
from api.storage.database.messages import Messages
from api.storage.database.users import Users


class ISearchStorage(ABC):
    @abc.abstractmethod
    async def messages_by_text(self, text: str) -> list[Messages]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def users_by_name(self, name: str) -> list[Users]:
        raise NotImplementedError()
