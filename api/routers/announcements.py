import logging
from datetime import datetime

from fastapi import APIRouter, Depends

from api.announcements.announcement_producer import AnnouncementProducer
from api.models.db.user import User
from api.models.key_value.announcement import Announcement
from api.models.key_value.statement import Statement
from api.queue.models.announce_task import AnnounceTask
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.interface.announcements import IAnnouncementStorage
from api.storage.interface.friends import IFriendsStorage
from api.storage.key_value.announcement import AnnouncementRedisStorage
from api.models.key_value.announcements import Announcements

logger = logging.getLogger(__name__)


class AnnouncementsRouter(APIRouter):
    def __init__(
        self,
        friends_storage: IFriendsStorage,
        jwt_middleware: JWTMiddleware,
        announcement_redis_storage: AnnouncementRedisStorage,
        announcement_producer: AnnouncementProducer,
        announcement_storage: IAnnouncementStorage,
    ):
        super().__init__()
        self.tags = ["announcements"]

        @self.get("/announcements")
        async def get_announcements(
            user: User = Depends(jwt_middleware.get_user()),
        ) -> Announcements:
            logger.debug("Getting announcements of user %s", user)

            announcements = await announcement_redis_storage.get_announcements(user.id)

            return announcements

        @self.post("/announcement")
        async def post_announcement(
            content: str,
            user: User = Depends(jwt_middleware.get_user()),
        ) -> list[User]:
            friends = await friends_storage.get_friends_for(user.id)
            announcement = Announcement(
                statement=Statement(content=content),
                by=user.id,
                at=datetime.now(),
            )

            logger.debug(
                "Saving Announcement %s into db for user %s", announcement, user
            )
            await announcement_storage.add_announcement(
                user_id=user.id, announcement=announcement
            )

            logger.debug(
                "Announcing %s for firends %s of user %s", announcement, friends, user
            )
            tasks = []
            for friend in friends:
                task = AnnounceTask(
                    announcement=announcement,
                    to=friend,
                )
                tasks.append(task)

            return await announcement_producer.announce(tasks=tasks)
