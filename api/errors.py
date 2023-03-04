class UserNotFoundError(Exception):
    pass


class ChatNotFoundError(Exception):
    pass


class NotAuthorizedError(Exception):
    def __init__(self, message: str = "Not authorized"):
        super().__init__(message)


class NotAuthenticatedError(Exception):
    def __init__(self, message: str = "Not authenticated"):
        super().__init__(message)
