import logging

from api.announcements.announcement_consumer import AnnouncementConsumer
from api.announcements.announcement_producer import AnnouncementProducer
from api.app import App
from api.prometheus.manager import PrometheusManager
from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.queue.consumer import Consumer
from api.queue.producer import Producer
from api.queue.settings import QueueSettings, AnnouncementQueueSettings
from api.routers.announcements import AnnouncementsRouter
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.metrics import MetricsRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer, JWTCookie
from api.routers.search import SearchRouter
from api.routers.users import UsersRouter
from api.storage.database.announcements import AnnouncementStorage
from api.storage.database.chat import ChatStorage
from api.storage.database.friends import FriendsStorage
from api.storage.database.manager import DatabaseManager
from api.storage.database.search import SearchStorage
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage
from api.storage.key_value.announcement import AnnouncementRedisStorage
from api.storage.key_value.base import RedisSettings

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(message)s",
)

postgres_settings = PostgresSettings()
database_manager = DatabaseManager(postgres_settings=postgres_settings)
users_storage = UsersStorage(database_manager=database_manager)
friends_storage = FriendsStorage(database_manager=database_manager)
chat_storage = ChatStorage(database_manager=database_manager)

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

search_storage = SearchStorage(database_manager=database_manager)
search_router = SearchRouter(
    search_storage=search_storage,
    friends_storage=friends_storage,
    jwt_middleware=jwt_middleware,
)

prometheus_manager = PrometheusManager()
metrics_router = MetricsRouter(prometheus_manager=prometheus_manager)

queue_settings = AnnouncementQueueSettings()
producer = Producer(queue_settings=queue_settings)
redis_settings = RedisSettings()
announcement_redis_storage = AnnouncementRedisStorage(redis_settings=redis_settings)
announcement_producer = AnnouncementProducer(producer=producer)
announcement_storage = AnnouncementStorage(database_manager=database_manager)
announcements_router = AnnouncementsRouter(
    friends_storage=friends_storage,
    jwt_middleware=jwt_middleware,
    announcement_producer=announcement_producer,
    announcement_redis_storage=announcement_redis_storage,
    announcement_storage=announcement_storage,
)

app = App(
    users_router=users_router,
    friends_router=friends_router,
    login_router=login_router,
    chat_router=chat_router,
    search_router=search_router,
    metrics_router=metrics_router,
    database_manager=database_manager,
    prometheus_manager=prometheus_manager,
    announcements_router=announcements_router,
)
