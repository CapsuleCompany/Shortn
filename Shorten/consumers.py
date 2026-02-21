"""
Kafka consumers for the Shorten service.

Listens for auth events so the Shorten service can react to user lifecycle
changes (e.g. log activity, initialize per-user resources, clean up on delete).
"""

import logging

from events.consumer import EventConsumer
from events.topics import Topics

logger = logging.getLogger(__name__)


class AuthEventConsumer(EventConsumer):
    """Processes auth-related events for the Shorten service."""

    topics = [
        Topics.AUTH_USER_REGISTERED,
        Topics.AUTH_USER_LOGGED_IN,
    ]
    group_id = "shorten-service"

    def handle(self, event: dict) -> None:
        event_type = event.get("event_type")
        data = event.get("data", {})

        if event_type == "user.registered":
            logger.info(
                "New user registered: %s (id=%s) — ready to create short URLs",
                data.get("username"),
                data.get("user_id"),
            )

        elif event_type == "user.logged_in":
            logger.info(
                "User logged in: %s (id=%s)",
                data.get("username"),
                data.get("user_id"),
            )
