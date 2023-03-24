import requests

from api.models.api.login_request import LoginRequest
from tests.utils import get_random_email


url = "http://localhost:8000"


with requests.Session() as client:
    email = get_random_email()
    user_creation_res = client.post(
        url=f"{url}/users/",
        json={
            "name": "Alice",
            "age": 0,
            "about": "string",
            "email": email,
            "password": "string",
        },
    )

    friend_creation_res = client.post(
        url=f"{url}/users/",
        json={
            "name": "Bob",
            "age": 0,
            "about": "string",
            "email": get_random_email(),
            "password": "string",
        },
    )
    login_request = LoginRequest(email=email, password="string")
    login_response = client.post(url=f"{url}/login/", json=login_request.dict())
    print(login_response.headers)

    friend_user_id = friend_creation_res.json()
    client.post(
        url=f"{url}/friends/add/{friend_user_id}",
    )

    client.post(
        url=f"{url}/chat/start/{friend_user_id}",
    )
