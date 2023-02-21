from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from api.models.api.login_request import LoginRequest
from api.storage.friends import FriendsStorage


@pytest.fixture()
def prepare_users(client: TestClient):
    for i in range(3):
        client.post(
            "/users/",
            json={
                "name": "string",
                "age": 0,
                "about": "string",
                "email": f"string{i}",
                "password": "string",
            },
        )


class TestFriendAPI:
    @pytest.mark.parametrize(
        "user_id, friend_id",
        [
            (0, 1),
            (2, 0),
        ],
    )
    def test_add_friend(
        self,
        client: TestClient,
        user_id: int,
        friend_id: int,
        friends_storage: FriendsStorage,
            prepare_users,
    ):
        client.post("/login/", json=LoginRequest(email=f'string{user_id}', password='string').dict())

        res = client.post(f"/friends/add/{friend_id}")

        assert res.status_code == HTTPStatus.OK
        assert friends_storage.get_friends() == {(user_id, friend_id), (friend_id, user_id)}

    @pytest.mark.parametrize(
        "user_id, friend_id",
        [
            (0, 1),
            (2, 0),
        ],
    )
    def test_cannot_add_friend_when_already_added(
        self,
        client: TestClient,
        user_id: int,
        friend_id: int,
        friends_storage: FriendsStorage,
            prepare_users,
    ):
        client.post("/login/", json=LoginRequest(email=f'string{user_id}', password='string').dict())

        res = client.post(f"/friends/add/{friend_id}")

        assert res.status_code == HTTPStatus.OK

        with pytest.raises(Exception):
            client.post(f"/friends/add/{friend_id}")

        assert friends_storage.get_friends() == {(user_id, friend_id),
                                                 (friend_id, user_id)}

