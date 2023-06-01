import os

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette_exporter import PrometheusMiddleware

from api.errors import UserNotFoundError, NotAuthorizedError, NotAuthenticatedError
from api.prometheus.manager import PrometheusManager
from api.routers.announcements import AnnouncementsRouter
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.metrics import MetricsRouter
from api.routers.search import SearchRouter
from api.routers.users import UsersRouter
from api.storage.database.manager import DatabaseManager


class App(FastAPI):
    def __init__(
        self,
        users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter,
        chat_router: ChatRouter,
        search_router: SearchRouter,
        metrics_router: MetricsRouter,
        database_manager: DatabaseManager,
        prometheus_manager: PrometheusManager,
        announcements_router: AnnouncementsRouter,
    ):
        super().__init__(title=os.environ.get("HOSTNAME"))
        self.include_router(users_router)
        self.include_router(friends_router)
        self.include_router(login_router)
        self.include_router(chat_router)
        self.include_router(search_router)

        self.include_router(metrics_router)
        self.add_middleware(PrometheusMiddleware)

        self.include_router(announcements_router)

        self.exception_handler(UserNotFoundError)(self._user_not_found_handler_error)
        self.exception_handler(NotAuthorizedError)(self._bad_auth_error)
        self.exception_handler(NotAuthenticatedError)(self._bad_auth_error)
        self.exception_handler(Exception)(self._server_error)

        self._database_manager = database_manager
        self._prometheus_manager = prometheus_manager

        self.on_event("startup")(self._on_startup)
        self.on_event("shutdown")(self._on_shutdown)

    async def _on_startup(self):
        await self._database_manager.connect()

    async def _on_shutdown(self):
        await self._database_manager.disconnect()

    async def _user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)

    async def _bad_auth_error(self, request, exc):
        return JSONResponse(str(exc), status_code=401)

    async def _server_error(self, request, exc):
        return JSONResponse(str(exc), status_code=503)
