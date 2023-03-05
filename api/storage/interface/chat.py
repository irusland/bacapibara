import abc

from api.models.api.chat import Chat


class IChatStorage(abc.ABC):
    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_chat(self, user_ids: list[int]) -> Chat:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_chat(self, chat_id: int) -> Chat:
        raise NotImplementedError()
