class AnyStr(str):
    """A Class primarily for comparing a raw password with hashed one."""
    def __eq__(self, x: object) -> bool:
        return True
