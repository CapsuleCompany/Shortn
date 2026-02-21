import random
import string
import uuid

from django.conf import settings
from django.db import models


def generate_short_code():
    """Generate a unique short code with configurable length."""
    length = getattr(settings, "SHORT_CODE_LENGTH", 6)
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


class ShortenedURL(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    original_url = models.URLField()
    short_code = models.CharField(
        max_length=20, unique=True, default=generate_short_code, db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)
    ip_address = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"
