from fastapi import FastAPI
from sqlalchemy import URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from starlette.responses import JSONResponse

from api.errors import UserNotFoundError, NotAuthorizedError, NotAuthenticatedError
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.users import UsersRouter
from api.storage.database.base import Base
from api.storage.database.settings import PostgresSettings


class DatabaseManager:
    def __init__(self, postgres_settings: PostgresSettings):

        self.engine = create_async_engine(
            postgres_settings.connect_url,
            echo=True,
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def connect(self):
        print(f">>> startup start")
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print(f">>> startup end")

    async def disconnect(self):
        await self.engine.dispose()


class App(FastAPI):
    def __init__(
        self,
        users_router: UsersRouter,
        friends_router: FriendsRouter,
        login_router: LoginRouter,
        chat_router: ChatRouter,
        database_manager: DatabaseManager,
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

        self._database_manager = database_manager
        self.on_event("startup")(self._database_manager.connect)
        self.on_event("shutdown")(self._database_manager.disconnect)

    async def _user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)

    async def _bad_auth_error(self, request, exc):
        return JSONResponse(str(exc), status_code=401)

    async def _server_error(self, request, exc):
        return JSONResponse(str(exc), status_code=503)
