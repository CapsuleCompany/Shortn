import logging

from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from events import EventProducer
from events.schemas import token_refreshed, user_logged_in, user_registered
from events.topics import Topics

from .serializers import RegisterSerializer

logger = logging.getLogger(__name__)


class RegisterView(CreateAPIView):
    """API endpoint for user registration."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        EventProducer.get_instance().send(
            Topics.AUTH_USER_REGISTERED,
            user_registered(user.id, user.username, user.email),
            key=str(user.id),
        )


class LoginView(TokenObtainPairView):
    """JWT login that emits a ``user.logged_in`` event on success."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            username = request.data.get("username", "")
            try:
                user = User.objects.get(username=username)
                EventProducer.get_instance().send(
                    Topics.AUTH_USER_LOGGED_IN,
                    user_logged_in(user.id, user.username),
                    key=str(user.id),
                )
            except User.DoesNotExist:
                logger.warning("Login event skipped — user %s not found", username)
        return response


class RefreshView(TokenRefreshView):
    """JWT token refresh that emits a ``token.refreshed`` event on success."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200 and request.user.is_authenticated:
            EventProducer.get_instance().send(
                Topics.AUTH_TOKEN_REFRESHED,
                token_refreshed(request.user.id, request.user.username),
                key=str(request.user.id),
            )
        return response
