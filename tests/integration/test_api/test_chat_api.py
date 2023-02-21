from http import HTTPStatus

import pytest
from starlette.testclient import TestClient

from api.models.api.login_request import LoginRequest
from api.storage.chat import ChatStorage
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


class TestChatAPI:
    @pytest.mark.parametrize(
        "user_id, friend_id",
        [
            (0, 1),
            (2, 0),
        ],
    )
    def test_create_chat(
        self,
        client: TestClient,
        user_id: int,
        friend_id: int,
        chat_storage: ChatStorage,
            prepare_users,
    ):
        client.post("/login/", json=LoginRequest(email=f'string{user_id}', password='string').dict())
        client.post(f"/friends/add/{friend_id}")

        res = client.post(f"/chat/start/{friend_id}")

        assert res.status_code == HTTPStatus.OK
        assert chat_storage.get_chat(0)
