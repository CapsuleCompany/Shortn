"""Middleware for automatic request/response event logging."""

import time

from core.logging import event_logger


def _get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class RequestLoggingMiddleware:
    """Log every completed HTTP request as a structured JSON event.

    Captures method, path, status code, response time, client IP, and
    authenticated user — everything a cloud logging dashboard needs for
    traffic analysis and alerting.

    Add to ``MIDDLEWARE`` in settings::

        "core.middleware.RequestLoggingMiddleware",
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        start = time.monotonic()
        response = self.get_response(request)
        duration_ms = (time.monotonic() - start) * 1000

        user = None
        if hasattr(request, "user") and request.user.is_authenticated:
            user = request.user.username

        event_logger.request_finished(
            method=request.method,
            path=request.get_full_path(),
            status_code=response.status_code,
            duration_ms=duration_ms,
            ip_address=_get_client_ip(request),
            user=user,
        )

        return response
