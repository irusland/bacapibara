import abc

from api.models.key_value.announcement import Announcement


class IAnnouncementStorage(abc.ABC):
    @abc.abstractmethod
    async def size(self) -> int:
        raise NotImplementedError()

    @abc.abstractmethod
    async def add_announcement(self, user_id: int, announcement: Announcement):
        raise NotImplementedError()
