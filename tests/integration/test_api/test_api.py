import pytest
from starlette.testclient import TestClient

from api.main import App
from api.routers.friends import FriendsRouter
from api.routers.users import UsersRouter
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage


@pytest.fixture()
def app() -> App:
    user_storage = UsersStorage()
    users_router = UsersRouter(user_storage=user_storage)
    friends_storage = FriendsStorage()
    friends_router = FriendsRouter(friends_storage=friends_storage)
    return App(users_router=users_router, friends_router=friends_router)


@pytest.fixture()
def client(app: App) -> TestClient:
    return TestClient(app)


class TestAPI:
    def test_get_users(self, client: TestClient):
        res = client.get('/users')

        assert res
