from kombu import Connection
from tracardi_plugin_sdk.domain.register import Plugin, Spec, MetaData
from tracardi_plugin_sdk.action_runner import ActionRunner

from tracardi.domain.entity import Entity
from tracardi.domain.source import Source, SourceRecord
from tracardi_rabbitmq_publisher.model.queue_config import QueueConfig
from tracardi_rabbitmq_publisher.model.rabbit_configuration import RabbitSourceConfiguration
from tracardi_rabbitmq_publisher.service.queue_publisher import QueuePublisher


class RabbitPublisherAction(ActionRunner):

    @staticmethod
    async def build(**kwargs) -> 'RabbitPublisherAction':
        plugin = RabbitPublisherAction(**kwargs)
        source_config_record = await Entity(id=plugin.source).\
            storage('source').\
            load(SourceRecord)  # type: SourceRecord

        if source_config_record is None:
            raise ValueError('Source id {} does not exist.'.format(plugin.source))

        source_config = source_config_record.decode()

        plugin.source = RabbitSourceConfiguration(
            **source_config.config
        )

        return plugin

    def __init__(self, *args, **kwargs):
        if 'source' not in kwargs:
            raise ValueError('Source not defined.')

        if 'id' not in kwargs['source'] or kwargs['source']['id'] is None:
            raise ValueError('Source id not defined.')

        self.source = kwargs['source']['id']

        # load queue_config info

        if 'queue' not in kwargs:
            raise ValueError('Queue not defined.')

        if 'name' not in kwargs['queue'] or kwargs['queue']['name'] is None:
            raise ValueError('Queue name not defined.')

        if 'routingKey' not in kwargs['queue'] or kwargs['queue']['routingKey'] is None:
            raise ValueError('routingKey name not defined.')

        self.queue = QueueConfig(
            name=kwargs['queue']['name'],
            routing_key=kwargs['queue']['routingKey']
        )

    async def run(self, payload):
        with Connection(self.source.uri, connect_timeout=self.source.timeout) as conn:
            queue_publisher = QueuePublisher(conn, queue_config=self.queue)
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
            version='0.1',
            license="MIT",
            author="Risto Kowaczewski",
            init={
                "source": {
                    "id": None
                },
                "queue": {
                    "name": None,
                    "routingKey": None,
                    "queue_type": "direct",
                    "compression": None
                }
            }

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
