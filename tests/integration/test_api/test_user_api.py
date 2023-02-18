from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from api.models.api.new_user import NewUser
from api.models.api.user import User
from api.models.db.user import User as DBUser
from api.storage.users import UsersStorage


@pytest.fixture()
def new_user() -> NewUser:
    return NewUser(
        name="irusland",
        age=42,
        email="irusland@mail.ru",
        about="It's me",
        password="capibara",
    )


@pytest.fixture()
def test_user(new_user: NewUser) -> User:
    return User(
        id=0,
        name=new_user.name,
        age=new_user.age,
        email=new_user.email,
        about=new_user.about,
        password=new_user.password,
    )


@pytest.fixture()
def db_user(test_user: User) -> DBUser:
    return DBUser(
        id=test_user.id,
        name=test_user.name,
        age=test_user.age,
        email=test_user.email,
        about=test_user.about,
        password=test_user.password,
    )


class TestUserAPI:
    def test_get_users(self, client: TestClient):
        res = client.get("/users")

        assert res.status_code == HTTPStatus.OK

    def test_create_user(
        self,
        client: TestClient,
        user_storage: UsersStorage,
        new_user: NewUser,
        test_user: User,
        db_user: DBUser,
    ):
        expected_user = db_user

        res = client.post("/users", json=new_user.dict())

        assert res.status_code == HTTPStatus.OK
        assert res.json() == expected_user.id
        assert user_storage.get_users() == [expected_user]

    def test_get_user(
        self, client: TestClient, user_storage: UsersStorage, test_user: User
    ):
        expected_user = test_user
        client.post("/users", json=expected_user.dict())
        user_id = expected_user.id

        res = client.get(f"/users/{user_id}")

        assert res.status_code == HTTPStatus.OK
        assert User.parse_obj(res.json()) == expected_user

    def test_update_user(
        self, client: TestClient, user_storage: UsersStorage, new_user: NewUser
    ):
        client.post("/users", json=new_user.dict())
        new_user = User(
            id=0,
            name="england",
            age=1337,
            email="england@mail.ru",
            about="It is not me",
            password="capi",
        )
        user_id = new_user.id

        res = client.put(f"/users/{user_id}", json=new_user.dict())

        assert res.status_code == HTTPStatus.OK
        assert user_storage.get_users() == [
            DBUser(
                id=new_user.id,
                name=new_user.name,
                age=new_user.age,
                email=new_user.email,
                about=new_user.about,
                password=new_user.password,
            )
        ]
