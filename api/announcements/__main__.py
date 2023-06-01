import asyncio

from api.announcements.announcement_consumer import AnnouncementConsumer
from api.queue.consumer import Consumer
from api.queue.settings import AnnouncementQueueSettings
from api.storage.key_value.announcement import AnnouncementRedisStorage
from api.storage.key_value.base import RedisSettings

queue_settings = AnnouncementQueueSettings()
consumer = Consumer(queue_settings=queue_settings)
redis_settings = RedisSettings()
announcement_redis_storage = AnnouncementRedisStorage(redis_settings=redis_settings)
announcement_consumer = AnnouncementConsumer(
    consumer=consumer,
    announcement_redis_storage=announcement_redis_storage,
)

asyncio.run(announcement_consumer.process())
