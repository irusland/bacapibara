import aio_pika

from api.queue.settings import QueueSettings


class Producer:
    def __init__(self, queue_settings: QueueSettings):
        self._queue_settings = queue_settings

    async def produce(self, messages: list[str]):
        connection = await aio_pika.connect_robust(self._queue_settings.url)
        async with connection:
            channel = await connection.channel()

            for message in messages:
                await channel.default_exchange.publish(
                    aio_pika.Message(body=message.encode()),
                    routing_key=self._queue_settings.queue,
                )
