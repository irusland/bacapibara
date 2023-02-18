from fastapi import APIRouter

from api.models.api.new_user import NewUser
from api.models.api.user import User as APIUser
from api.models.db.user import User as DBUser
from api.storage.users import UsersStorage


class UsersRouter(APIRouter):
    def __init__(self, user_storage: UsersStorage):
        super().__init__()
        self.tags = ["users"]

        @self.post("/users/", response_model=int)
        async def create_user(user: NewUser):
            new_user = DBUser(
                id=len(user_storage),
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
            return user_storage.create_user(new_user).id

        @self.get("/users/", response_model=list[APIUser])
        async def get_users():
            return [
                APIUser(
                    id=user.id,
                    name=user.name,
                    about=user.about,
                    age=user.age,
                    email=user.email,
                    password=user.password,
                )
                for user in user_storage.get_users()
            ]

        @self.get("/users/{id}")
        async def get_user(id: int):
            user = user_storage.get_user(id_=id)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )

        @self.put("/users/{id}", response_model=APIUser)
        async def update_user(id: int, user: NewUser):
            new_user = DBUser(
                id=id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
            user = user_storage.update_user(id, new_user)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
