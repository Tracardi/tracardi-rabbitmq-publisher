import asyncio
from tracardi_rabbitmq_publisher.plugin import RabbitPublisherAction

async def main():
    plugin = await RabbitPublisherAction.build(
        **{
            "source": {
                "id": "58df3b5c-3109-4750-bb5b-81f5386950b1"
            },
            "queue": {
                "name": "tracardi3",
                "routingKey": "trk",
            }
        }
    )

    await plugin.run({"a": 1})

asyncio.run(main())
