"""
Event payload schemas for Kafka messages.

Each function returns a dict that will be JSON-serialized and sent as
the Kafka message value. Using plain dicts keeps the events module
dependency-free (no DRF serializers needed).
"""

import uuid
from datetime import datetime, timezone


def _base_envelope(event_type: str, data: dict) -> dict:
    """Wrap every event in a standard envelope."""
    return {
        "event_id": str(uuid.uuid4()),
        "event_type": event_type,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "data": data,
    }


def user_registered(user_id: int, username: str, email: str) -> dict:
    return _base_envelope(
        "user.registered",
        {
            "user_id": user_id,
            "username": username,
            "email": email,
        },
    )


def user_logged_in(user_id: int, username: str) -> dict:
    return _base_envelope(
        "user.logged_in",
        {
            "user_id": user_id,
            "username": username,
        },
    )


def token_refreshed(user_id: int, username: str) -> dict:
    return _base_envelope(
        "token.refreshed",
        {
            "user_id": user_id,
            "username": username,
        },
    )
