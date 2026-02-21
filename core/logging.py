"""Structured event logging for cloud deployments.

Emits JSON-formatted log entries that are automatically parsed by cloud logging
services (Google Cloud Logging, AWS CloudWatch, Azure Monitor, etc.).

Usage:
    from core.logging import event_logger

    event_logger.log("url_created", short_code="abc123", original_url="https://example.com")
    event_logger.log("url_redirected", short_code="abc123", cached=True)
"""

import logging
import time

from pythonjsonlogger import json as json_log


class CloudJsonFormatter(json_log.JsonFormatter):
    """JSON formatter tuned for cloud log ingestion.

    Adds ``severity`` (the Google Cloud Logging convention that AWS and Azure
    also understand) and ``timestamp`` to every record so that cloud agents can
    index and filter without extra configuration.
    """

    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        log_record["severity"] = record.levelname
        log_record["logger"] = record.name
        log_record["timestamp"] = self.formatTime(record)


class EventLogger:
    """Thin wrapper that attaches structured ``extra`` fields to log calls."""

    def __init__(self, name: str = "shortn.events"):
        self._logger = logging.getLogger(name)

    # ------------------------------------------------------------------
    # Public helpers
    # ------------------------------------------------------------------

    def log(self, event: str, *, level: int = logging.INFO, **extra):
        """Emit a structured event log entry.

        Parameters
        ----------
        event:
            A short, dot-free identifier such as ``url_created`` or
            ``auth_login_success``.
        level:
            Standard logging level (default ``INFO``).
        **extra:
            Arbitrary key/value pairs attached to the JSON payload.
        """
        self._logger.log(level, event, extra={"event": event, **extra})

    def url_created(self, *, short_code: str, original_url: str, ip_address: str | None = None, user: str | None = None):
        self.log(
            "url_created",
            short_code=short_code,
            original_url=original_url,
            ip_address=ip_address,
            user=user,
        )

    def url_redirected(self, *, short_code: str, cached: bool = False):
        self.log("url_redirected", short_code=short_code, cached=cached)

    def url_analytics_viewed(self, *, short_code: str, cached: bool = False):
        self.log("url_analytics_viewed", short_code=short_code, cached=cached)

    def auth_register(self, *, username: str):
        self.log("auth_register", username=username)

    def auth_login(self, *, username: str, success: bool):
        level = logging.INFO if success else logging.WARNING
        self.log("auth_login", level=level, username=username, success=success)

    def qr_generated(self, *, url: str, has_logo: bool = False):
        self.log("qr_generated", url=url, has_logo=has_logo)

    def request_finished(self, *, method: str, path: str, status_code: int, duration_ms: float, ip_address: str | None = None, user: str | None = None):
        level = logging.WARNING if status_code >= 400 else logging.INFO
        self.log(
            "request_finished",
            level=level,
            method=method,
            path=path,
            status_code=status_code,
            duration_ms=round(duration_ms, 2),
            ip_address=ip_address,
            user=user,
        )


event_logger = EventLogger()
