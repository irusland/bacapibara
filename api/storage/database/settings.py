from pydantic import BaseSettings
from sqlalchemy import URL


class PostgresSettings(BaseSettings):
    db: str
    user: str
    password: str
    host: str
    port: int = 5432
    driver: str = "postgresql+asyncpg"

    @property
    def connect_url(self) -> URL:
        return URL(
            drivername=self.driver,
            database=self.db,
            username=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
            query={},
        )

    class Config:
        env_prefix = "POSTGRES_"
