from pydantic import BaseSettings


class QueueSettings(BaseSettings):
    url: str
    queue: str
    consume_batch: int = 10


class AnnouncementQueueSettings(QueueSettings):
    queue: str = "irusland_announcements"

    class Config:
        env_prefix = "ANNOUNCEMENT_QUEUE_"
