from pydantic import BaseSettings


class JWTSettings(BaseSettings):
    secret: str = "irusland"
    algorithm: str = "HS256"
    session_cookie_key: str = "session"

    class Config:
        env_prefix = "JWT_"
