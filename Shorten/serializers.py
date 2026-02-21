from django.conf import settings
from rest_framework import serializers

from .models import ShortenedURL


class ShortenedURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()

    class Meta:
        model = ShortenedURL
        fields = ["id", "original_url", "short_code", "short_url", "created_at", "click_count"]
        read_only_fields = ["short_code", "created_at", "click_count"]

    def get_short_url(self, obj):
        base = getattr(settings, "BASE_URL", "http://localhost:8000").rstrip("/")
        return f"{base}/{obj.short_code}/"
