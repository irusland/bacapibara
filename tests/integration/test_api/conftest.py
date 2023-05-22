from typing import Iterator
from unittest.mock import Mock

import pytest
import pytest_asyncio
from starlette.testclient import TestClient

from api.announcements.announcement_producer import AnnouncementProducer
from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.app import App
from api.prometheus.manager import PrometheusManager
from api.queue.producer import Producer
from api.queue.settings import QueueSettings, AnnouncementQueueSettings
from api.routers.announcements import AnnouncementsRouter
from api.routers.metrics import MetricsRouter
from api.routers.search import SearchRouter
from api.storage.database.manager import DatabaseManager
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer, JWTCookie
from api.routers.users import UsersRouter
from api.storage.database.search import SearchStorage
from api.storage.interface.announcements import IAnnouncementStorage
from api.storage.interface.friends import IFriendsStorage
from api.storage.key_value.announcement import AnnouncementRedisStorage
from api.storage.key_value.base import RedisSettings
from api.storage.memory.chat import ChatStorage
from api.storage.memory.friends import FriendsStorage
from api.storage.memory.users import UsersStorage


from asgi_lifespan import LifespanManager
from httpx import AsyncClient


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
def database_manager() -> DatabaseManager:
    return Mock(DatabaseManager)


@pytest.fixture(scope="session")
def prometheus_manager() -> PrometheusManager:
    return PrometheusManager()


@pytest.fixture()
def metrics_router(prometheus_manager: PrometheusManager) -> MetricsRouter:
    return MetricsRouter(prometheus_manager=prometheus_manager)


@pytest.fixture()
def search_storage(database_manager: DatabaseManager) -> SearchStorage:
    return SearchStorage(database_manager=database_manager)


@pytest.fixture()
def search_router(
    search_storage: SearchStorage,
    friends_storage: FriendsStorage,
    jwt_middleware: JWTMiddleware,
) -> SearchRouter:
    return SearchRouter(
        search_storage=search_storage,
        friends_storage=friends_storage,
        jwt_middleware=jwt_middleware,
    )


@pytest.fixture()
def redis_settings() -> RedisSettings:
    return RedisSettings()


@pytest.fixture()
def announcement_redis_storage(
    redis_settings: RedisSettings,
) -> AnnouncementRedisStorage:
    announcement_redis_storage = AnnouncementRedisStorage(
        redis_settings=redis_settings,
    )
    redis = {}

    async def _set(key, value):
        redis[key] = value

    announcement_redis_storage._set = Mock(wraps=_set)

    async def _get(key):
        return redis.get(key)

    announcement_redis_storage._get = Mock(wraps=_get)
    return announcement_redis_storage


@pytest.fixture()
def queue_settings() -> AnnouncementQueueSettings:
    return AnnouncementQueueSettings()


@pytest.fixture()
def producer(
    queue_settings: QueueSettings,
) -> Producer:
    return Mock(Producer)


@pytest.fixture()
def announcement_storage() -> IAnnouncementStorage:
    return Mock(IAnnouncementStorage)


@pytest.fixture()
def announcement_producer(
    producer: Producer,
) -> AnnouncementProducer:
    return AnnouncementProducer(
        producer=producer,
    )


@pytest.fixture()
def announcements_router(
    friends_storage: IFriendsStorage,
    jwt_middleware: JWTMiddleware,
    announcement_redis_storage: AnnouncementRedisStorage,
    announcement_producer: AnnouncementProducer,
    announcement_storage: IAnnouncementStorage,
) -> AnnouncementsRouter:
    return AnnouncementsRouter(
        friends_storage=friends_storage,
        jwt_middleware=jwt_middleware,
        announcement_redis_storage=announcement_redis_storage,
        announcement_producer=announcement_producer,
        announcement_storage=announcement_storage,
    )


@pytest.fixture()
def app(
    users_router: UsersRouter,
    friends_router: FriendsRouter,
    chat_router: ChatRouter,
    login_router: LoginRouter,
    metrics_router: MetricsRouter,
    search_router: SearchRouter,
    database_manager: DatabaseManager,
    prometheus_manager: PrometheusManager,
    announcements_router: AnnouncementsRouter,
) -> App:
    return App(
        users_router=users_router,
        friends_router=friends_router,
        chat_router=chat_router,
        login_router=login_router,
        metrics_router=metrics_router,
        search_router=search_router,
        database_manager=database_manager,
        prometheus_manager=prometheus_manager,
        announcements_router=announcements_router,
    )


@pytest.fixture()
def client(app: App) -> TestClient:
    return TestClient(app)


@pytest_asyncio.fixture()
async def async_client(app: App) -> Iterator[AsyncClient]:
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client
