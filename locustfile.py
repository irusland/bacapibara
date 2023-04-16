import uuid

from locust import HttpUser, task
import requests


class BaraUser(HttpUser):
    def __init__(self, parent):
        super().__init__(parent)

        email = uuid.uuid4().hex
        password = uuid.uuid4().hex

        res = requests.post(
            f"{self.host}/users",
            json={
                "name": "string",
                "age": 0,
                "about": "string",
                "email": email,
                "password": password,
            },
            verify=False,
        )
        assert res.ok
        self._user_id = int(res.text)
        print("Load test as user", self._user_id)

        login_res = requests.post(
            f"{self.host}/login",
            json={"email": email, "password": password},
            verify=False,
        )
        session = login_res.headers["set-cookie"].split("=")[1]
        self._cookies = {"session": session}

    def on_start(self):
        """on_start is called when a Locust start before any task is scheduled"""
        self.client.verify = False

    @task
    def users(self):
        self.client.get("/users", cookies=self._cookies)

    @task
    def user(self):
        self.client.get(f"/users/{self._user_id}", cookies=self._cookies)

    @task
    def update_user(self):
        self.client.put(
            f"/users/{self._user_id}",
            cookies=self._cookies,
            json={
                "name": "string",
                "age": 0,
                "about": "string",
                "email": "string",
                "password": "string",
            },
        )

    @task
    def search_user(self):
        self.client.get("/search/users/руслан", cookies=self._cookies)

    @task
    def search_messages(self):
        self.client.get("/search/messages/руслан", cookies=self._cookies)
