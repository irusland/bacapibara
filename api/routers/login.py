import logging

import bcrypt
from fastapi import APIRouter
from fastapi import Response

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.errors import NotAuthenticatedError
from api.models.api.login_request import LoginRequest
from api.storage.users import UsersStorage

logger = logging.getLogger(__name__)


class LoginRouter(APIRouter):
    def __init__(
        self,
        user_storage: UsersStorage,
        jwt_manager: JWTManager,
        jwt_settings: JWTSettings,
    ):
        super().__init__()
        self.tags = ["login"]

        @self.post("/login/")
        async def login(login_request: LoginRequest, response: Response):
            user = user_storage.find_user(login_request.email)
            if bcrypt.checkpw(login_request.password.encode(), user.password.encode()):
                response.set_cookie(
                    key=jwt_settings.session_cookie_key,
                    value=jwt_manager.encode(user_id=user.id),
                )
                return {"message": f"User {user} was authenticated"}
            logger.info("User entered wrong password")
            raise NotAuthenticatedError()
