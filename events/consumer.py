"""
Kafka event consumer base class.

Subclass EventConsumer and implement ``handle(event)`` to process messages.

Usage:
    class MyConsumer(EventConsumer):
        topics = [Topics.AUTH_USER_REGISTERED]
        group_id = "shorten-service"

        def handle(self, event: dict) -> None:
            print(event["data"]["username"])

    MyConsumer().run()
"""

import json
import logging
import signal
import sys

from confluent_kafka import Consumer, KafkaError
from django.conf import settings

logger = logging.getLogger(__name__)


class EventConsumer:
    """Abstract base consumer — subclass and override ``handle``."""

    topics: list[str] = []
    group_id: str = "default"

    def __init__(self):
        bootstrap = getattr(settings, "KAFKA_BOOTSTRAP_SERVERS", "")
        if not bootstrap:
            raise RuntimeError("KAFKA_BOOTSTRAP_SERVERS is not configured")

        self._consumer = Consumer({
            "bootstrap.servers": bootstrap,
            "group.id": self.group_id,
            "auto.offset.reset": "earliest",
            "enable.auto.commit": True,
        })
        self._running = True

    def handle(self, event: dict) -> None:
        """Override this in subclasses to process a deserialized event."""
        raise NotImplementedError

    def run(self, poll_timeout: float = 1.0) -> None:
        """Subscribe and poll in a loop until interrupted."""
        self._consumer.subscribe(self.topics)
        logger.info(
            "Consumer [%s] subscribed to %s", self.group_id, self.topics
        )

        # Graceful shutdown on SIGINT / SIGTERM
        def _stop(signum, frame):
            logger.info("Received signal %s — shutting down consumer", signum)
            self._running = False

        signal.signal(signal.SIGINT, _stop)
        signal.signal(signal.SIGTERM, _stop)

        try:
            while self._running:
                msg = self._consumer.poll(poll_timeout)
                if msg is None:
                    continue

                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        continue
                    logger.error("Consumer error: %s", msg.error())
                    continue

                try:
                    event = json.loads(msg.value().decode("utf-8"))
                    logger.info(
                        "Received %s from %s",
                        event.get("event_type", "unknown"),
                        msg.topic(),
                    )
                    self.handle(event)
                except Exception:
                    logger.exception(
                        "Failed to handle message from %s", msg.topic()
                    )
        finally:
            self._consumer.close()
            logger.info("Consumer [%s] closed", self.group_id)
