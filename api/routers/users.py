from fastapi import APIRouter

from api.models.user import User
from api.storage.users import UsersStorage


class UsersRouter(APIRouter):
    def __init__(self, user_storage: UsersStorage):
        super().__init__()
        self.tags = ["users"]

        @self.post("/users/", response_model=int)
        async def create_user(name: str, about: str, age: int, email: str):
            new_user = User(
                id=len(user_storage),
                name=name,
                about=about,
                age=age,
                email=email,
            )
            return user_storage.create_user(new_user).id

        @self.get("/users/", response_model=list[User])
        async def get_users():
            return user_storage.get_users()

        @self.get("/users/{id}")
        async def get_user(id: int):
            return user_storage.get_user(id_=id)

        @self.put("/users/{id}", response_model=User)
        async def update_user(id: int, name: str, about: str, age: int, email: str):
            new_user = User(
                id=id,
                name=name,
                about=about,
                age=age,
                email=email,
            )
            return user_storage.update_user(id, new_user)
