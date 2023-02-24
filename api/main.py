import logging

from fastapi import FastAPI
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.errors import UserNotFoundError, NotAuthorizedError, NotAuthenticatedError
from api.models.api.login_request import LoginRequest
from api.routers import login
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer, JWTCookie
from api.routers.users import UsersRouter
from api.storage.chat import ChatStorage
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(message)s",
)


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


users_storage = UsersStorage()
friends_storage = FriendsStorage()
chat_storage = ChatStorage()

jwt_settings = JWTSettings()
jwt_manager = JWTManager(jwt_settings=jwt_settings)
jwt_bearer = JWTBearer(jwt_manager=jwt_manager, jwt_settings=jwt_settings)
jwt_cookie = JWTCookie(jwt_manager=jwt_manager, jwt_settings=jwt_settings)
jwt_middleware = JWTMiddleware(
    jwt_manager=jwt_manager,
    jwt_bearer=jwt_bearer,
    jwt_settings=jwt_settings,
    jwt_cookie=jwt_cookie,
    users_storage=users_storage,
)

web_socket_connection_manager = WebSocketConnectionManager()

users_router = UsersRouter(
    users_storage=users_storage,
    jwt_middleware=jwt_middleware,
)
friends_router = FriendsRouter(
    friends_storage=friends_storage,
    jwt_middleware=jwt_middleware,
    users_storage=users_storage,
)
login_router = LoginRouter(
    users_storage=users_storage, jwt_manager=jwt_manager, jwt_settings=jwt_settings
)
chat_router = ChatRouter(
    users_storage=users_storage,
    friends_storage=friends_storage,
    jwt_manager=jwt_manager,
    jwt_settings=jwt_settings,
    jwt_middleware=jwt_middleware,
    chat_storage=chat_storage,
    web_socket_connection_manager=web_socket_connection_manager,
)

app = App(
    users_router=users_router,
    friends_router=friends_router,
    login_router=login_router,
    chat_router=chat_router,
)


client = TestClient(app)
res = client.post(
    "/users/",
    json={
        "name": "Alice",
        "age": 0,
        "about": "string",
        "email": "string",
        "password": "string",
    },
)

client.post(
    "/users/",
    json={
        "name": "Bob",
        "age": 0,
        "about": "string",
        "email": "string2",
        "password": "string",
    },
)
login_request = LoginRequest(email="string", password="string")
login_response = client.post("/login/", json=login_request.dict())
print(login_response.headers)

client.post(
    "/friends/add/1",
)


client.post(
    "/chat/start/1",
)
