from typing import Any

import jwt

from api.auth.jwt_settings import JWTSettings
from api.models.api.user_credentials import UserCredentials


class JWTManager:
    def __init__(self, jwt_settings: JWTSettings):
        self._jwt_settings = jwt_settings

    def encode(
        self,
        user_id: int,
    ) -> str:
        return jwt.encode(
            payload=UserCredentials(id=user_id).dict(),
            key=self._jwt_settings.secret,
            algorithm=self._jwt_settings.algorithm,
        )

    def decode(self, encoded_jwt: str) -> Any:
        try:
            return jwt.decode(
                jwt=encoded_jwt,
                key=self._jwt_settings.secret,
                algorithms=[self._jwt_settings.algorithm],
            )
        except:
            return None
