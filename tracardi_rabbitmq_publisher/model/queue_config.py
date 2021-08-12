from pydantic import BaseModel


class QueueConfig(BaseModel):
    durable: bool = True
    queue_type: str = 'direct'
    routing_key: str
    name: str
    compression: str = None
