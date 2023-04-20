import abc

from api.models.api.chat import Chat

from api.storage.message import Message


class IChatStorage(abc.ABC):
    @abc.abstractmethod
    async def size(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def create_chat(self, user_ids: list[int]) -> Chat:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_chat(self, chat_id: int) -> Chat:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_message(self, chat_id: int, message: Message) -> None:
        raise NotImplementedError()
