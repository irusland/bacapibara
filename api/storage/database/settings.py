from pydantic import BaseSettings


class PostgresSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int = 5432
    driver: str = 'postgresql+asyncpg'

    class Config:
        env_prefix = "POSTGRES_"
