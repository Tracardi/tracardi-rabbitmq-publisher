from tracardi_rabbitmq_publisher.plugin import RabbitPublisherAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

init = {
            "source": {
                "id": "a4fb18a2-5406-4190-bd91-e1719bb5202c"
            },
            "queue": {
                "name": "tracardi-1",
                "routingKey": "trk",
            }
        }

payload = {"a": 1}

result = run_plugin(RabbitPublisherAction, init, payload)
