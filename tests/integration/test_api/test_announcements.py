from http import HTTPStatus

import pytest
from httpx import AsyncClient
from starlette.testclient import TestClient

from api.models.api.login_request import LoginRequest
from api.storage.interface.friends import IFriendsStorage


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


@pytest.mark.asyncio
class TestAnnouncements:
    @pytest.mark.parametrize(
        "user_id, friend_id",
        [
            (0, 1),
            (2, 0),
        ],
    )
    async def test_announcement(
        self,
        async_client: AsyncClient,
        user_id: int,
        friend_id: int,
        friends_storage: IFriendsStorage,
        prepare_users,
    ):
        await async_client.post(
            "/login/",
            json=LoginRequest(email=f"string{user_id}", password="string").dict(),
        )

        res = await async_client.post(f"/friends/add/{friend_id}")

        assert res.status_code == HTTPStatus.OK
        assert await friends_storage.get_friends() == {
            (user_id, friend_id),
            (friend_id, user_id),
        }

        res = await async_client.post(
            "/announcement",
            params={'content': 'привет!'},
        )

        assert res.status_code == HTTPStatus.OK

        res = await async_client.get(
            "/announcements",
        )

        assert res.status_code == HTTPStatus.OK

        await async_client.post(
            "/login/",
            json=LoginRequest(email=f"string{friend_id}", password="string").dict(),
        )

        res = await async_client.get(
            "/announcements",
        )

        assert res.status_code == HTTPStatus.OK
