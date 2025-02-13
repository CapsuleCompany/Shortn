from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics
from rest_framework.views import APIView
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer


class CreateShortURL(generics.CreateAPIView):
    """Create a new shortened URL"""
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer


class RedirectShortURL(APIView):
    """Redirect a short URL to the original URL"""
    def get(self, request, short_code):
        url = get_object_or_404(ShortenedURL, short_code=short_code)
        url.click_count += 1
        url.save()
        return redirect(url.original_url)


class URLAnalytics(generics.RetrieveAPIView):
    """Retrieve analytics for a shortened URL"""
    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = "short_code"