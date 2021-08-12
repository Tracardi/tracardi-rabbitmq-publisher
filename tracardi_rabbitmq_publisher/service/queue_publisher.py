import logging
from kombu import Exchange, Queue, Producer
from ..model.queue_config import QueueConfig

logging.basicConfig(format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class QueuePublisher:

    def __init__(self, conn, queue_config: QueueConfig):
        self.conn = conn
        self.queue_config = queue_config
        channel = conn.channel()
        exchange = Exchange(queue_config.name, queue_config.queue_type, durable=queue_config.durable)
        queue = Queue(queue_config.name, exchange=exchange, routing_key=queue_config.routing_key)
        queue.maybe_bind(self.conn)
        queue.declare()

        self.producer = Producer(exchange=exchange,
                                 channel=channel,
                                 routing_key=queue.routing_key,
                                 serializer='json',
                                 auto_declare=True)

    def publish(self, payload):
        self.producer.publish(payload)  # , compression='bzip2'
