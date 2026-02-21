from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from .models import ShortenedURL


class ShortenModelTest(TestCase):
    def test_create_shortened_url(self):
        url = ShortenedURL.objects.create(original_url="https://example.com")
        self.assertEqual(len(url.short_code), 6)
        self.assertEqual(url.click_count, 0)
        self.assertEqual(url.original_url, "https://example.com")

    def test_short_code_is_unique(self):
        url1 = ShortenedURL.objects.create(original_url="https://example.com")
        url2 = ShortenedURL.objects.create(original_url="https://example.org")
        self.assertNotEqual(url1.short_code, url2.short_code)


class CreateShortURLTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_shorten_url(self):
        response = self.client.post("/shorten/", {"original_url": "https://example.com"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("short_code", response.data)
        self.assertIn("short_url", response.data)

    def test_shorten_url_invalid(self):
        response = self.client.post("/shorten/", {"original_url": "not-a-url"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class RedirectShortURLTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = ShortenedURL.objects.create(original_url="https://example.com")

    def test_redirect(self):
        response = self.client.get(f"/{self.url.short_code}/")
        self.assertEqual(response.status_code, status.HTTP_302_FOUND)
        self.assertEqual(response["Location"], "https://example.com")

    def test_redirect_increments_click_count(self):
        self.client.get(f"/{self.url.short_code}/")
        self.url.refresh_from_db()
        self.assertEqual(self.url.click_count, 1)

    def test_redirect_not_found(self):
        response = self.client.get("/nonexistent/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class URLAnalyticsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = ShortenedURL.objects.create(
            original_url="https://example.com", click_count=42
        )

    def test_analytics(self):
        response = self.client.get(f"/analytics/{self.url.short_code}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["click_count"], 42)

    def test_analytics_not_found(self):
        response = self.client.get("/analytics/nope123/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class URLListTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        ShortenedURL.objects.create(original_url="https://a.com", click_count=5)
        ShortenedURL.objects.create(original_url="https://b.com", click_count=15)

    def test_list_urls(self):
        response = self.client.get("/urls/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_urls"], 2)

    def test_filter_min_clicks(self):
        response = self.client.get("/urls/?min_clicks=10")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_urls"], 1)


class HealthCheckTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_health(self):
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "healthy")

    def test_api_info(self):
        response = self.client.get("/", HTTP_ACCEPT="application/json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["service"], "Shortn")
