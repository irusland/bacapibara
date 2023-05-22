import logging

from api.queue.models.announce_task import AnnounceTask
from api.queue.producer import Producer
from api.storage.key_value.announcement import AnnouncementRedisStorage

logger = logging.getLogger(__name__)


class AnnouncementProducer:
    def __init__(
        self, producer: Producer, announcement_redis_storage: AnnouncementRedisStorage
    ):
        self._producer = producer
        self._announcement_redis_storage = announcement_redis_storage

    async def announce(self, tasks: list[AnnounceTask]):
        logger.info("Announcing tasks %s", tasks)

        await self._producer.produce(messages=[task.json() for task in tasks])
