import asyncio

from kombu import Connection, Exchange, Queue, Producer

from tracardi_rabbitmq_publisher.model.queue_config import QueueConfig
from tracardi_rabbitmq_publisher.plugin import RabbitPublisherAction

async def main():
    plugin = await RabbitPublisherAction.build(
        **{
            "source": {
                "id": "d0956a79-b885-4e6d-bda5-7f77e614bc2b"
            },
            "queue": {
                "name": "tracardi2",
                "routingKey": "trk",
            }
        }
    )

    await plugin.run({"a": 1})

asyncio.run(main())
