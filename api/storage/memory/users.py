from api.errors import UserNotFoundError
from api.models.db.user import User
from api.storage.interface.users import IUsersStorage


class UsersStorage(IUsersStorage):
    def __init__(self):
        self._users = {}

    def __len__(self) -> int:
        return len(self._users)

    def create_user(self, user: User) -> User:
        if user.id in self._users:
            raise Exception(f"User id={user.id} already exists")

        try:
            self.find_user(email=user.email)
        except UserNotFoundError:
            pass
        else:
            raise Exception(f"User email={user.email} already exists")

        self._users[user.id] = user

        return user

    def get_users(self) -> list[User]:
        return [user for user in self._users.values()]

    def get_user(self, id_: int) -> User:
        if id_ not in self._users:
            raise UserNotFoundError(f"User id={id_} was not found")

        return self._users[id_]

    def update_user(self, id_: int, new_user: User) -> User:
        if id_ not in self._users:
            raise UserNotFoundError(f"User id={id_} was not found")

        self._users[id_] = new_user
        return new_user

    def find_user(self, email: str) -> User:
        for id, user in self._users.items():
            if user.email == email:
                return user

        raise UserNotFoundError(f"User was not found")

    def on_user_login(self, user: User) -> None:
        pass
