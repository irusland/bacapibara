import logging

from fastapi import APIRouter, Depends

from api.models.db.user import User
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.interface.friends import IFriendsStorage
from api.storage.interface.users import IUsersStorage

logger = logging.getLogger(__name__)


class FriendsRouter(APIRouter):
    def __init__(
        self,
        friends_storage: IFriendsStorage,
        users_storage: IUsersStorage,
        jwt_middleware: JWTMiddleware,
    ):
        super().__init__()
        self.prefix = "/friends"
        self.tags = [self.prefix]

        @self.post("/add/{friend_id}")
        async def add_friendship(
            friend_id: int,
            user: User = Depends(jwt_middleware.get_user()),
        ):
            friend = await users_storage.get_user(friend_id)
            logger.debug("user %s adding user %s", user.id, friend.id)
            return await friends_storage.add_friend(user.id, friend.id)
