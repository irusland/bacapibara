import pytest
from starlette.testclient import TestClient

from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.main import App
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer, JWTCookie
from api.routers.users import UsersRouter
from api.storage.chat import ChatStorage
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage


@pytest.fixture()
def users_storage() -> UsersStorage:
    return UsersStorage()


@pytest.fixture()
def friends_storage() -> FriendsStorage:
    return FriendsStorage()


@pytest.fixture()
def chat_storage() -> ChatStorage:
    return ChatStorage()


@pytest.fixture()
def jwt_settings() -> JWTSettings:
    return JWTSettings()


@pytest.fixture()
def jwt_bearer(jwt_manager: JWTManager, jwt_settings: JWTSettings) -> JWTBearer:
    return JWTBearer(jwt_manager=jwt_manager, jwt_settings=jwt_settings)


@pytest.fixture()
def jwt_cookie(jwt_manager: JWTManager, jwt_settings: JWTSettings) -> JWTCookie:
    return JWTCookie(jwt_manager=jwt_manager, jwt_settings=jwt_settings)


@pytest.fixture()
def web_socket_connection_manager() -> WebSocketConnectionManager:
    return WebSocketConnectionManager()


@pytest.fixture()
def chat_router(
    users_storage: UsersStorage,
    friends_storage: FriendsStorage,
    jwt_manager: JWTManager,
    jwt_settings: JWTSettings,
    jwt_middleware: JWTMiddleware,
    chat_storage: ChatStorage,
    web_socket_connection_manager: WebSocketConnectionManager,
) -> ChatRouter:
    return ChatRouter(
        jwt_manager=jwt_manager,
        jwt_settings=jwt_settings,
        chat_storage=chat_storage,
        jwt_middleware=jwt_middleware,
        users_storage=users_storage,
        friends_storage=friends_storage,
        web_socket_connection_manager=web_socket_connection_manager,
    )


@pytest.fixture()
def jwt_manager(jwt_settings: JWTSettings) -> JWTManager:
    return JWTManager(jwt_settings=jwt_settings)


@pytest.fixture()
def jwt_middleware(
    jwt_manager: JWTManager,
    jwt_bearer: JWTBearer,
    jwt_cookie: JWTCookie,
    jwt_settings: JWTSettings,
    users_storage: UsersStorage,
) -> JWTMiddleware:
    return JWTMiddleware(
        jwt_manager=jwt_manager,
        jwt_bearer=jwt_bearer,
        jwt_cookie=jwt_cookie,
        jwt_settings=jwt_settings,
        users_storage=users_storage,
    )


@pytest.fixture()
def users_router(
    users_storage: UsersStorage, jwt_middleware: JWTMiddleware
) -> UsersRouter:
    return UsersRouter(users_storage=users_storage, jwt_middleware=jwt_middleware)


@pytest.fixture()
def friends_router(
    friends_storage: FriendsStorage,
    jwt_middleware: JWTMiddleware,
    users_storage: UsersStorage,
) -> FriendsRouter:
    return FriendsRouter(
        friends_storage=friends_storage,
        jwt_middleware=jwt_middleware,
        users_storage=users_storage,
    )


@pytest.fixture()
def login_router(
    users_storage: UsersStorage,
    jwt_manager: JWTManager,
    jwt_settings: JWTSettings,
) -> LoginRouter:
    return LoginRouter(
        users_storage=users_storage, jwt_manager=jwt_manager, jwt_settings=jwt_settings
    )


@pytest.fixture()
def app(
    users_router: UsersRouter,
    friends_router: FriendsRouter,
    chat_router: ChatRouter,
    login_router: LoginRouter,
) -> App:
    return App(
        users_router=users_router,
        friends_router=friends_router,
        chat_router=chat_router,
        login_router=login_router,
    )


@pytest.fixture()
def client(app: App) -> TestClient:
    return TestClient(app)
