import logging

from fastapi import APIRouter, Depends

from api.models.db.user import User
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.interface.friends import IFriendsStorage
from api.storage.interface.search import ISearchStorage
from api.storage.interface.users import IUsersStorage
from api.storage.message import Message

logger = logging.getLogger(__name__)


class SearchRouter(APIRouter):
    def __init__(
        self,
        search_storage: ISearchStorage,
        friends_storage: IFriendsStorage,
        jwt_middleware: JWTMiddleware,
    ):
        super().__init__()
        self.prefix = "/search"
        self.tags = [self.prefix]

        @self.get("/messages/{text}")
        async def search_messages(
            text: str,
            user: User = Depends(jwt_middleware.get_user()),
        ) -> list[Message]:
            friends = await friends_storage.get_friends_for(user.id)
            logger.debug("Searching messages from friends %s of user %s", friends, user)

            messages = await search_storage.messages_by_text(text)
            filtered_messages = []
            for message in messages:
                if message.user_id in friends:
                    filtered_messages.append(
                        Message(user_id=message.user_id, text=message.text)
                    )

            return filtered_messages
