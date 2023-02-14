import pytest
from starlette.testclient import TestClient

from api.main import App
from api.routers.friends import FriendsRouter
from api.routers.users import UsersRouter
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage


@pytest.fixture()
def user_storage() -> UsersStorage:
    return UsersStorage()


@pytest.fixture()
def friends_storage() -> FriendsStorage:
    return FriendsStorage()


@pytest.fixture()
def users_router(user_storage: UsersStorage) -> UsersRouter:
    return UsersRouter(user_storage=user_storage)


@pytest.fixture()
def friends_router(friends_storage: FriendsStorage) -> FriendsRouter:
    return FriendsRouter(friends_storage=friends_storage)


@pytest.fixture()
def app(users_router: UsersRouter, friends_router: FriendsRouter) -> App:
    return App(users_router=users_router, friends_router=friends_router)


@pytest.fixture()
def client(app: App) -> TestClient:
    return TestClient(app)
