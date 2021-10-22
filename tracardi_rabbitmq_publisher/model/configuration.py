from typing import Optional

from pydantic import BaseModel
from tracardi.domain.entity import Entity


class QueueConfig(BaseModel):
    durable: bool = True
    queue_type: str = 'direct'
    routing_key: str
    name: str
    compression: Optional[str] = None
    auto_declare: bool = True
    serializer: str = 'json'


class PluginConfiguration(BaseModel):
    source: Entity
    queue: QueueConfig
