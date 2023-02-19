from typing import Any

from fastapi import APIRouter, Request, Depends
from fastapi.security import HTTPBearer

from api.auth.jwt_manager import JWTManager
from api.models.api.new_user import NewUser
from api.models.api.user import User as APIUser
from api.models.db.user import User as DBUser
from api.routers.middlewares.jwt import JWTMiddleware, AuthGroup, JWTBearer
from api.storage.users import UsersStorage
import bcrypt


class UsersRouter(APIRouter):
    def __init__(
        self,
        user_storage: UsersStorage,
        jwt_middleware: JWTMiddleware,
        jwt_bearer: JWTBearer,
    ):
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
                password=bcrypt.hashpw(
                    user.password.encode(), bcrypt.gensalt()
                ).decode(),
            )
            return user_storage.create_user(new_user).id

        @self.get(
            "/users/",
            response_model=list[APIUser],
            dependencies=[
                # Depends(jwt_middleware.ensure_has_rights([AuthGroup.ADMIN])),
                Depends(jwt_bearer),
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
                for user in user_storage.get_users()
            ]

        @self.get(
            "/users/{id}",
            response_model=APIUser,
            dependencies=[Depends(jwt_middleware.ensure_has_rights([AuthGroup.USER]))],
        )
        async def get_user(id: int) -> APIUser:
            user = user_storage.get_user(id_=id)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )

        @self.put(
            "/users/{id}",
            response_model=APIUser,
            dependencies=[Depends(jwt_middleware.ensure_has_rights([AuthGroup.USER]))],
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
            user = user_storage.update_user(id, new_user)
            return APIUser(
                id=user.id,
                name=user.name,
                about=user.about,
                age=user.age,
                email=user.email,
                password=user.password,
            )
