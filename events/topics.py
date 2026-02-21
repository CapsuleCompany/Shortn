"""
Kafka topic constants for inter-service communication.

Naming convention: <service>.<entity>.<action>
"""


class Topics:
    # Auth service events
    AUTH_USER_REGISTERED = "auth.user.registered"
    AUTH_USER_LOGGED_IN = "auth.user.logged_in"
    AUTH_TOKEN_REFRESHED = "auth.token.refreshed"
