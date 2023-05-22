from pydantic import BaseSettings

from api.models.api.user_id import UserId
from api.models.key_value.announcements import Announcements
from api.models.key_value.announcement import Announcement
from api.storage.key_value.base import BaseRedisStorage, RedisSettings


class AnnouncementRedisStorage(BaseRedisStorage):
    def __init__(self, redis_settings: RedisSettings):
        super().__init__(redis_settings)

    async def add_announcement(
        self, to: UserId, announcement: Announcement
    ) -> Announcements:
        key = str(to)
        container = Announcements.parse_raw(await self._get(key))
        container.announcements.append(announcement)
        await self._set(key, container.json())
        return container

    async def get_announcements(self, to: UserId) -> Announcements:
        key = str(to)
        value = await self._get(key)
        if value:
            return Announcements.parse_raw(value)
        return Announcements(announcements=[])
