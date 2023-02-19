import logging

from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.errors import UserNotFoundError, NotAuthorizedError, NotAuthenticatedError
from api.routers import login
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer
from api.routers.users import UsersRouter
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(message)s",
)


class App(FastAPI):
    def __init__(
        self,
        users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter,
    ):
        super().__init__()
        self.include_router(users_router)
        self.include_router(friends_router)
        self.include_router(login_router)
        self.exception_handler(UserNotFoundError)(self._user_not_found_handler_error)
        self.exception_handler(NotAuthorizedError)(self._bad_auth_error)
        self.exception_handler(NotAuthenticatedError)(self._bad_auth_error)

    async def _user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)

    async def _bad_auth_error(self, request, exc):
        return JSONResponse(str(exc), status_code=401)


jwt_settings = JWTSettings()
jwt_manager = JWTManager(jwt_settings=jwt_settings)
jwt_bearer = JWTBearer(jwt_manager=jwt_manager)
jwt_middleware = JWTMiddleware(jwt_manager=jwt_manager, jwt_bearer=jwt_bearer)
user_storage = UsersStorage()
friends_storage = FriendsStorage()

users_router = UsersRouter(
    user_storage=user_storage, jwt_middleware=jwt_middleware, jwt_bearer=jwt_bearer
)
friends_router = FriendsRouter(friends_storage=friends_storage)
login_router = LoginRouter(
    user_storage=user_storage, jwt_manager=jwt_manager, jwt_settings=jwt_settings
)

app = App(
    users_router=users_router, friends_router=friends_router, login_router=login_router
)
