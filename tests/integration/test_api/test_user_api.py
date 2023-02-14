from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from api.models.user import User
from api.storage.users import UsersStorage


@pytest.fixture()
def test_user() -> User:
    return User(
        id=0, name="irusland", age=42, email="irusland@mail.ru", about="It's me"
    )


class TestUserAPI:
    def test_get_users(self, client: TestClient):
        res = client.get("/users")

        assert res.status_code == HTTPStatus.OK

    def test_create_user(
        self, client: TestClient, user_storage: UsersStorage, test_user: User
    ):
        expected_user = test_user

        res = client.post("/users", params=expected_user.dict())

        assert res.status_code == HTTPStatus.OK
        assert res.json() == expected_user.id
        assert user_storage.get_users() == [expected_user]

    def test_get_user(
        self, client: TestClient, user_storage: UsersStorage, test_user: User
    ):
        expected_user = test_user
        client.post("/users", params=expected_user.dict())
        user_id = expected_user.id

        res = client.get(f"/users/{user_id}")

        assert res.status_code == HTTPStatus.OK
        assert User.parse_obj(res.json()) == expected_user

    def test_update_user(
        self, client: TestClient, user_storage: UsersStorage, test_user: User
    ):
        expected_user = test_user
        client.post("/users", params=expected_user.dict())
        new_user = User(
            id=0,
            name="england",
            age=1337,
            email="england@mail.ru",
            about="It is not me",
        )
        user_id = new_user.id

        res = client.put(f"/users/{user_id}", params=new_user.dict())

        assert res.status_code == HTTPStatus.OK
        assert user_storage.get_users() == [new_user]
