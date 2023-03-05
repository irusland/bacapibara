import logging

from starlette.testclient import TestClient

from api.app import App
from api.auth.jwt_manager import JWTManager
from api.auth.jwt_settings import JWTSettings
from api.connection.web_socket_connection_manager import WebSocketConnectionManager
from api.models.api.login_request import LoginRequest
from api.routers.chat import ChatRouter
from api.routers.friends import FriendsRouter
from api.routers.login import LoginRouter
from api.routers.middlewares.jwt import JWTMiddleware, JWTBearer, JWTCookie
from api.routers.users import UsersRouter
from api.storage.database.chat import ChatStorage
from api.storage.database.settings import PostgresSettings
from api.storage.database.users import UsersStorage
from api.storage.database.friends import FriendsStorage
from tests.utils import get_random_email

logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s: [%(asctime)s] p%(process)s {%(pathname)s:%(lineno)d} - %(message)s",
)

postgres_settings = PostgresSettings()
users_storage = UsersStorage(postgres_settings=postgres_settings)
friends_storage = FriendsStorage(postgres_settings=postgres_settings)
chat_storage = ChatStorage(postgres_settings=postgres_settings)

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
email = get_random_email()
res = client.post(
    "/users/",
    json={
        "name": "Alice",
        "age": 0,
        "about": "string",
        "email": email,
        "password": "string",
    },
)

client.post(
    "/users/",
    json={
        "name": "Bob",
        "age": 0,
        "about": "string",
        "email": get_random_email(),
        "password": "string",
    },
)
login_request = LoginRequest(email=email, password="string")
login_response = client.post("/login/", json=login_request.dict())
print(login_response.headers)

client.post(
    "/friends/add/1",
)

client.post(
    "/chat/start/1",
)
