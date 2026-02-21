from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny

from core.logging import event_logger

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    """API endpoint for user registration."""

    queryset = User.objects.all()
    permission_classes = [AllowAny]
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        user = serializer.save()
        event_logger.auth_register(username=user.username)