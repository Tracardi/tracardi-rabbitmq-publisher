from tracardi_rabbitmq_publisher.plugin import RabbitPublisherAction
from tracardi_plugin_sdk.service.plugin_runner import run_plugin

init = {
            "source": {
                "id": "74246646-f25e-4592-aea8-3fc383bc461a"
            },
            "queue": {
                "name": "tracardi-1",
                "routingKey": "trk",
            }
        }

payload = {"a": 1}

result = run_plugin(RabbitPublisherAction, init, payload)
