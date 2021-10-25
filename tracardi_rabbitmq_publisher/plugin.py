from kombu import Connection
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData, Form, FormGroup, FormField, FormComponent
from tracardi_plugin_sdk.action_runner import ActionRunner
from tracardi.service.storage.driver import storage
from tracardi_rabbitmq_publisher.model.configuration import PluginConfiguration
from tracardi_rabbitmq_publisher.model.rabbit_configuration import RabbitSourceConfiguration
from tracardi_rabbitmq_publisher.service.queue_publisher import QueuePublisher


def validate(config: dict) -> PluginConfiguration:
    return PluginConfiguration(**config)


class RabbitPublisherAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'RabbitPublisherAction':
        config = validate(kwargs)
        source = await storage.driver.resource.load(config.source.id)
        resource = RabbitSourceConfiguration(
            **source.config
        )

        return RabbitPublisherAction(config, resource)

    def __init__(self, config: PluginConfiguration, resource: RabbitSourceConfiguration):
        self.source = resource
        self.config = config
        if self.config.queue.compression == "none":
            self.config.queue.compression = None

    async def run(self, payload):
        with Connection(self.source.uri, connect_timeout=self.source.timeout) as conn:
            queue_publisher = QueuePublisher(conn, config=self.config)
            queue_publisher.publish(payload)

        return None


def register() -> Plugin:
    return Plugin(
        start=False,
        spec=Spec(
            module='tracardi_rabbitmq_publisher.plugin',
            className='RabbitPublisherAction',
            inputs=["payload"],
            outputs=[],
            version='0.6.0',
            license="MIT",
            author="Risto Kowaczewski",
            manual="rabbit_publisher_action",
            init={
                "source": {
                    "id": None
                },
                "queue": {
                    "name": None,
                    "routing_key": None,
                    "queue_type": "direct",
                    "compression": None,
                    "auto_declare": True,
                    "serializer": "json"
                }
            },
            form=Form(groups=[
                FormGroup(
                    name="RabbitMQ connection settings",
                    fields=[
                        FormField(
                            id="source",
                            name="RabbitMQ resource",
                            description="Select RabbitMQ resource. Authentication credentials will be used to "
                                        "connect to RabbitMQ server.",
                            component=FormComponent(
                                type="resource",
                                props={"label": "resource"})
                        )
                    ]
                )
                ,
                FormGroup(
                    name="RabbitMQ queue settings",
                    fields=[
                        FormField(
                            id="queue.name",
                            name="Queue name",
                            description="Type queue name where the payload will be sent.",
                            component=FormComponent(type="text", props={"label": "Queue name"})
                        ),
                        FormField(
                            id="queue.routing_key",
                            name="Routing key",
                            description="Type routing key name.",
                            component=FormComponent(type="text", props={"label": "Routing key"})
                        ),
                        FormField(
                            id="queue.auto_declare",
                            name="Auto create queue",
                            description="Create queue on first published message.",
                            component=FormComponent(type="bool", props={
                                "label": "Should RabbitMQ create queue if it does not exist."
                            })
                        ),
                        FormField(
                            id="queue.queue_type",
                            name="Queue type",
                            description="Select queue type.",
                            component=FormComponent(type="select", props={
                                "label": "Queue type",
                                "items": {
                                    "direct": "Direct",
                                    "fanout": "Fanout",
                                    "topic": "Topic",
                                    "headers": "Headers"
                                }
                            })
                        ),

                    ]),
                    FormGroup(
                        name="RabbitMQ advanced queue settings",
                        fields=[
                            FormField(
                                id="queue.serializer",
                                name="Serialization type",
                                description="Select serialization type.",
                                component=FormComponent(type="select", props={
                                    "label": "Serialization type",
                                    "items": {
                                        "json": "JSON",
                                        "xml": "XML",
                                    }
                                })
                            ),
                            FormField(
                                id="queue.compression",
                                name="Data compression",
                                description="Select if the data should be compressed and with what algorithm.",
                                component=FormComponent(type="select", props={
                                    "label": "Compression",
                                    "style": {"width": "200px"},
                                    "items": {
                                        "none": "No compression",
                                        "bzip2": "Compress with bzip2",
                                        "gzip": "Compress with gzip",
                                    }
                                })
                            )
                        ]
                    )
            ]),

        ),
        metadata=MetaData(
            name='Rabbit publisher',
            desc='Publishes payload to rabbitmq.',
            type='flowNode',
            width=200,
            height=100,
            icon='rabbitmq',
            group=["Connectors"]
        )
    )
