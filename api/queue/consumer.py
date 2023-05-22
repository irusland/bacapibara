from typing import AsyncIterable

import aio_pika

from api.queue.settings import QueueSettings


class Consumer:
    def __init__(self, queue_settings: QueueSettings):
        self._queue_settings = queue_settings

    async def messages(self) -> AsyncIterable[str]:
        connection = await aio_pika.connect_robust(self._queue_settings.url)
        async with connection:
            channel = await connection.channel()
            await channel.set_qos(prefetch_count=self._queue_settings.consume_batch)
            queue = await channel.declare_queue(self._queue_settings.queue, auto_delete=True)

            async for message in self._consume_loop(queue):
                yield message

    async def _consume_loop(self, queue):
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    print(message.body)
                    yield message.body.decode()
