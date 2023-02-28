from fastapi import FastAPI
from starlette.responses import JSONResponse

from api.errors import UserNotFoundError
from api.routers.friends import FriendsRouter
from api.routers.users import UsersRouter
from api.storage.friends import FriendsStorage
from api.storage.users import UsersStorage


class App(FastAPI):
    def __init__(self, users_router: UsersRouter, friends_router: FriendsRouter):
        super().__init__()
        self.include_router(users_router)
        self.include_router(friends_router)
        self.exception_handler(UserNotFoundError)(self.user_not_found_handler_error)

    async def user_not_found_handler_error(self, request, exc):
        return JSONResponse(str(exc), status_code=404)


user_storage = UsersStorage()
users_router = UsersRouter(user_storage=user_storage)
friends_storage = FriendsStorage()
friends_router = FriendsRouter(friends_storage=friends_storage)
app = App(users_router=users_router, friends_router=friends_router)
