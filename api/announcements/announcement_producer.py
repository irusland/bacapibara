import logging

from api.queue.models.announce_task import AnnounceTask
from api.queue.producer import Producer

logger = logging.getLogger(__name__)


class AnnouncementProducer:
    def __init__(self, producer: Producer):
        self._producer = producer

    async def announce(self, tasks: list[AnnounceTask]):
        logger.info("Announcing tasks %s", tasks)

        await self._producer.produce(messages=[task.json() for task in tasks])
