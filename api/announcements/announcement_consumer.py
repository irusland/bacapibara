import logging

from api.queue.consumer import Consumer
from api.queue.models.announce_task import AnnounceTask
from api.storage.key_value.announcement import AnnouncementRedisStorage

logger = logging.getLogger(__name__)


class AnnouncementConsumer:
    def __init__(
        self, consumer: Consumer, announcement_redis_storage: AnnouncementRedisStorage
    ):
        self._consumer = consumer
        self._announcement_redis_storage = announcement_redis_storage

    async def process(self):
        async for message in self._consumer.messages():
            task = AnnounceTask.parse_raw(message)
            logger.info("Consuming task %s", task)
            await self._announcement_redis_storage.add_announcement(
                to=task.to, announcement=task.announcement
            )
