import abc

from api.models.api.chat import Chat


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
