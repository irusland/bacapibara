import abc


class IFriendsStorage(abc.ABC):
    @abc.abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    def add_friend(self, id_: int, other_id: int) -> set[tuple[int, int]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_friends(self) -> set[tuple[int, int]]:
        raise NotImplementedError()

    @abc.abstractmethod
    def get_friends_for(self, id: int) -> list[int]:
        raise NotImplementedError()
