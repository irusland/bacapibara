from datetime import timedelta

from pydantic import BaseSettings, Field


class JWTSettings(BaseSettings):
    secret: str = "irusland"
    algorithm: str = "HS256"
    session_cookie_key: str = "session"
    session_cookie_expires: timedelta = timedelta(minutes=42)
    use_bearer: bool = Field(
        False,
        description="used to switch between cookie or bearer-header authentication.",
    )

    class Config:
        env_prefix = "JWT_"
