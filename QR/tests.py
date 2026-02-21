from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class GenerateQRCodeTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_qr(self):
        response = self.client.post("/qr/generate/", {"url": "https://example.com"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response["Content-Type"], "image/png")

    def test_generate_qr_no_url(self):
        response = self.client.post("/qr/generate/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
