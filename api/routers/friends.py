import logging

from fastapi import APIRouter, Depends

from api.models.api.user_credentials import UserCredentials
from api.models.db.user import User
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.memory.friends import FriendsStorage
from api.storage.memory.users import UsersStorage

logger = logging.getLogger(__name__)


class FriendsRouter(APIRouter):
    def __init__(
        self,
        friends_storage: FriendsStorage,
        users_storage: UsersStorage,
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
            friend = users_storage.get_user(friend_id)
            logger.debug("user %s adding user %s", user.id, friend.id)
            return friends_storage.add_friend(user.id, friend.id)
