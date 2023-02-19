import logging

from fastapi import APIRouter, Depends
from fastapi import HTTPException

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.models.api.user_credentials import UserCredentials
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage

logger = logging.getLogger(__name__)


class ChatRouter(APIRouter):
    def __init__(
        self,
        user_storage: UsersStorage,
        friends_storage: FriendsStorage,
        jwt_manager: JWTManager,
        jwt_settings: JWTSettings,
        jwt_middleware: JWTMiddleware,
    ):
        super().__init__()
        self.prefix = "/chat"
        self.tags = [self.prefix]

        @self.post(
            "/start/{friend_id}",
        )
        async def start(
            friend_id: int,
            credentials: UserCredentials = Depends(
                jwt_middleware.get_user_credentials()
            ),
        ):
            user = user_storage.get_user(credentials.id)
            logger.debug("user %s starting a chat", user)
            friends_ids = friends_storage.get_friends_for(id=user.id)
            if friend_id not in friends_ids:
                raise HTTPException(
                    status_code=422,
                    detail="Starting a chat with stranger is not allowed",
                )
