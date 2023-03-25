from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from api.storage.database.base import Base
from api.storage.database.settings import PostgresSettings


class DatabaseManager:
    def __init__(self, postgres_settings: PostgresSettings):
        self.engine = create_async_engine(
            postgres_settings.connect_url,
            echo=True,
        )
        self.async_session = async_sessionmaker(self.engine, expire_on_commit=False)

    async def connect(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def disconnect(self):
        await self.engine.dispose()
