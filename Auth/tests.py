from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient


class RegisterTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register(self):
        response = self.client.post(
            "/auth/register/",
            {"username": "testuser", "email": "test@example.com", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_duplicate_username(self):
        User.objects.create_user("testuser", "test@example.com", "testpass123")
        response = self.client.post(
            "/auth/register/",
            {"username": "testuser", "email": "test2@example.com", "password": "testpass456"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_short_password(self):
        response = self.client.post(
            "/auth/register/",
            {"username": "testuser", "email": "test@example.com", "password": "short"},
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User.objects.create_user("testuser", "test@example.com", "testpass123")

    def test_login(self):
        response = self.client.post(
            "/auth/login/", {"username": "testuser", "password": "testpass123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_invalid(self):
        response = self.client.post(
            "/auth/login/", {"username": "testuser", "password": "wrongpassword"}
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
