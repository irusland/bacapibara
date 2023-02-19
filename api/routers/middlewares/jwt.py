import enum
from typing import List, Any

from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette.requests import Request

from api.auth.jwt_manager import JWTManager
from api.errors import NotAuthorizedError


class AuthGroup(enum.Enum):
    USER = "USER"
    ADMIN = "ADMIN"


class JWTBearer(HTTPBearer):
    def __init__(self, jwt_manager: JWTManager, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)
        self._jwt_manager = jwt_manager

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(
            JWTBearer, self
        ).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(
                    status_code=403, detail="Invalid authentication scheme."
                )
            if not self._jwt_manager.decode(credentials.credentials):
                raise HTTPException(
                    status_code=403, detail="Invalid token or expired token."
                )
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")


class JWTMiddleware:
    def __init__(self, jwt_manager: JWTManager, jwt_bearer: JWTBearer):
        self._jwt_manager = jwt_manager
        self._jwt_bearer = jwt_bearer

    def ensure_has_rights(self, required_groups: List[AuthGroup]):
        async def _ensure_has_rights(request: Request) -> Any:
            print(f">>> {request=}")
            print(f">>> {required_groups=}")
            credentials = await self._jwt_bearer.__call__(request)
            print(credentials)
            if AuthGroup.ADMIN in required_groups:
                raise NotAuthorizedError()
            return "ok"

        return _ensure_has_rights
