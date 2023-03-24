import abc


class IFriendsStorage(abc.ABC):
    @abc.abstractmethod
    async def size(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_friend(self, id_: int, other_id: int) -> set[tuple[int, int]]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_friends(self) -> set[tuple[int, int]]:
        raise NotImplementedError()

    @abc.abstractmethod
    async def get_friends_for(self, id: int) -> list[int]:
        raise NotImplementedError()
