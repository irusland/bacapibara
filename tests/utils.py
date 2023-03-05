from uuid import uuid4


class AnyStr(str):
    """A Class primarily for comparing a raw password with hashed one."""

    def __eq__(self, x: object) -> bool:
        return True


def get_random_email() -> str:
    return f"test_{uuid4().hex}@mail.ru"
