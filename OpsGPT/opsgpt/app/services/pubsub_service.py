from typing import Dict, Any, Callable, List
import threading
import logging
from app.config.settings import Settings

logger = logging.getLogger(__name__)


class PubSubClient:
    def publish(self, topic: str, message: Dict[str, Any]) -> str:
        raise NotImplementedError()


class InMemoryPubSub(PubSubClient):
    def __init__(self):
        self.topics: Dict[str, List[Dict[str, Any]]] = {}
        self.lock = threading.Lock()

    def publish(self, topic: str, message: Dict[str, Any]) -> str:
        with self.lock:
            self.topics.setdefault(topic, []).append(message)
        logger.info("Published message to topic %s: %s", topic, message.get("incident_id"))
        return message.get("incident_id", "")

    def pull(self, topic: str) -> List[Dict[str, Any]]:
        with self.lock:
            return list(self.topics.get(topic, []))

    def clear(self, topic: str) -> None:
        with self.lock:
            self.topics[topic] = []


def get_pubsub_client(settings: Settings) -> PubSubClient:
    if settings.LOCAL_MODE:
        return InMemoryPubSub()
    # Placeholder for real GCP Pub/Sub client (Phase 3)
    raise NotImplementedError("GCP Pub/Sub client not implemented yet")
