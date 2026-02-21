"""
Kafka consumers for the QR service.

Listens for auth events so the QR service can react to user lifecycle changes.
"""

import logging

from events.consumer import EventConsumer
from events.topics import Topics

logger = logging.getLogger(__name__)


class AuthEventConsumer(EventConsumer):
    """Processes auth-related events for the QR service."""

    topics = [
        Topics.AUTH_USER_REGISTERED,
    ]
    group_id = "qr-service"

    def handle(self, event: dict) -> None:
        event_type = event.get("event_type")
        data = event.get("data", {})

        if event_type == "user.registered":
            logger.info(
                "New user registered: %s (id=%s) — QR service notified",
                data.get("username"),
                data.get("user_id"),
            )
