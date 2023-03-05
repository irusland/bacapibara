from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str

    class Config:
        env_prefix = "POSTGRES_"
