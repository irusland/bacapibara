import bcrypt
from fastapi import APIRouter, Depends

from api.models.api.new_user import NewUser
from api.models.api.user import User as APIUser
from api.models.db.user import User as DBUser
from api.routers.middlewares.jwt import JWTMiddleware
from api.storage.users import UsersStorage


class UsersRouter(APIRouter):
    def __init__(
        self,
        users_storage: UsersStorage,
        jwt_middleware: JWTMiddleware,
    ):
        super().__init__()
        self.prefix = "/users"
        self.tags = [self.prefix]

        @self.post("/", response_model=int)
        async def create_user(user: NewUser):
            new_user = DBUser(
                id=len(users_storage),
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=bcrypt.hashpw(
                    user.password.encode(), bcrypt.gensalt()
                ).decode(),
            )
            return users_storage.create_user(new_user).id

        @self.get(
            "/",
            response_model=list[APIUser],
            dependencies=[
                Depends(jwt_middleware.get_user_credentials()),
            ],
        )
        async def get_users() -> list[APIUser]:
            return [
                APIUser(
                    id=user.id,
                    name=user.name,
                    about=user.about,
                    age=user.age,
                    email=user.email,
                    password=user.password,
                )
                for user in users_storage.get_users()
            ]

        @self.get(
            "/{id}",
            response_model=APIUser,
            dependencies=[Depends(jwt_middleware.get_user_credentials())],
        )
        async def get_user(id: int) -> APIUser:
            user = users_storage.get_user(id_=id)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )

        @self.put(
            "/{id}",
            response_model=APIUser,
            dependencies=[Depends(jwt_middleware.get_user_credentials())],
        )
        async def update_user(id: int, user: NewUser) -> APIUser:
            new_user = DBUser(
                id=id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
            user = users_storage.update_user(id, new_user)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
