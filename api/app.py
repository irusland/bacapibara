from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.errors import UserNotFoundError, NotAuthorizedError, NotAuthenticatedError
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.users import UsersRouter


class App(FastAPI):
    def __init__(
        self,
        users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter,
        chat_router: ChatRouter,
    ):
        super().__init__()
        self.include_router(users_router)
        self.include_router(friends_router)
        self.include_router(login_router)
        self.include_router(chat_router)

        self.exception_handler(UserNotFoundError)(self._user_not_found_handler_error)
        self.exception_handler(NotAuthorizedError)(self._bad_auth_error)
        self.exception_handler(NotAuthenticatedError)(self._bad_auth_error)
        self.exception_handler(Exception)(self._server_error)

    async def _user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)

    async def _bad_auth_error(self, request, exc):
        return JSONResponse(str(exc), status_code=401)

    async def _server_error(self, request, exc):
        return JSONResponse(str(exc), status_code=503)
