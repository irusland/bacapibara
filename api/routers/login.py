import datetime
import logging
from datetime import UTC

import bcrypt
from fastapi import APIRouter
from fastapi import Response

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.errors import NotAuthenticatedError
from api.models.api.login_request import LoginRequest
from api.storage.interface.users import IUsersStorage

logger = logging.getLogger(__name__)


class LoginRouter(APIRouter):
    def __init__(
        self,
        users_storage: IUsersStorage,
        jwt_manager: JWTManager,
        jwt_settings: JWTSettings,
    ):
        super().__init__()
        self.prefix = "/login"
        self.tags = [self.prefix]

        @self.post("/")
        async def login(login_request: LoginRequest, response: Response):
            user = users_storage.find_user(login_request.email)
            if bcrypt.checkpw(login_request.password.encode(), user.password.encode()):
                response.set_cookie(
                    key=jwt_settings.session_cookie_key,
                    value=jwt_manager.encode(user_id=user.id),
                    expires=datetime.datetime.now(tz=UTC)
                    + jwt_settings.session_cookie_expires,
                )
                users_storage.on_user_login(user=user)
                return {"message": f"User {user} was authenticated"}
            logger.info("User entered wrong password")
            raise NotAuthenticatedError()
