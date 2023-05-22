import logging

import redis.asyncio as redis


from pydantic import BaseSettings

logger = logging.getLogger(__name__)


class RedisSettings(BaseSettings):
    url: str

    class Config:
        env_prefix = "REDIS_"


class BaseRedisStorage:
    def __init__(self, redis_settings: RedisSettings):
        self._redis_settings = redis_settings
        self._redis = redis.from_url("redis://localhost")

    async def _set(self, key: str, value: str):
        await self._redis.set(key, value)

    async def _get(self, key: str) -> str:
        return await self._redis.get(key)

    async def _set_batch(self, key_values: list[tuple[str, str]]):
        async with self._redis.pipeline(transaction=True) as pipe:
            for k, v in key_values:
                pipe = pipe.set(k, v)

            results = await pipe.execute(raise_on_error=True)
            logger.debug("Batch set results: %s", results)

    async def _get_batch(self, keys: list[str]) -> list[str]:
        async with self._redis.pipeline(transaction=True) as pipe:
            for k in keys:
                pipe = pipe.get(k)
            return await pipe.execute(raise_on_error=True)
