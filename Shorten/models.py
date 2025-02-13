import random
import string
from django.db import models


def generate_short_code():
    """Generate a unique 6-character short code."""
    return ''.join(random.choices(string.ascii_letters + string.digits, k=6))


class ShortenedURL(models.Model):
    original_url = models.URLField()
    short_code = models.CharField(max_length=10, unique=True, default=generate_short_code)
    created_at = models.DateTimeField(auto_now_add=True)
    click_count = models.IntegerField(default=0)  # Tracks how many times the short URL is clicked

    def __str__(self):
        return f"{self.short_code} → {self.original_url}"