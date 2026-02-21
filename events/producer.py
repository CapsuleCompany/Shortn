"""
Kafka event producer.

Usage:
    from events import EventProducer
    from events.schemas import user_registered
    from events.topics import Topics

    producer = EventProducer()
    producer.send(Topics.AUTH_USER_REGISTERED, user_registered(...))
"""

import json
import logging

from confluent_kafka import Producer
from django.conf import settings

logger = logging.getLogger(__name__)


class EventProducer:
    """Thin wrapper around confluent_kafka.Producer."""

    _instance: "EventProducer | None" = None

    def __init__(self):
        bootstrap = getattr(settings, "KAFKA_BOOTSTRAP_SERVERS", "")
        if not bootstrap:
            logger.warning("KAFKA_BOOTSTRAP_SERVERS not configured — events will be dropped")
            self._producer = None
            return

        self._producer = Producer({
            "bootstrap.servers": bootstrap,
            "client.id": getattr(settings, "KAFKA_CLIENT_ID", "shortn"),
            "acks": "all",
            "retries": 3,
            "retry.backoff.ms": 200,
        })

    @classmethod
    def get_instance(cls) -> "EventProducer":
        """Return a singleton producer so connections are reused."""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    def _on_delivery(self, err, msg):
        if err is not None:
            logger.error("Event delivery failed: %s", err)
        else:
            logger.debug(
                "Event delivered to %s [%d] @ %d",
                msg.topic(),
                msg.partition(),
                msg.offset(),
            )

    def send(self, topic: str, payload: dict, key: str | None = None) -> None:
        """Serialize *payload* as JSON and produce to *topic*."""
        if self._producer is None:
            logger.debug("No Kafka producer — dropping event on %s", topic)
            return

        value = json.dumps(payload).encode("utf-8")
        encoded_key = key.encode("utf-8") if key else None

        self._producer.produce(
            topic=topic,
            value=value,
            key=encoded_key,
            callback=self._on_delivery,
        )
        # Trigger delivery callbacks without blocking indefinitely.
        self._producer.poll(0)

    def flush(self, timeout: float = 5.0) -> None:
        """Block until all buffered messages are delivered."""
        if self._producer is not None:
            self._producer.flush(timeout)
