from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, viewsets, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ShortenedURL
from .serializers import ShortenedURLSerializer


class URLShortenerViewSet(viewsets.ModelViewSet):
    """
    Custom List View for shortened URLs with filtering, ordering, and custom response.
    """
    queryset = ShortenedURL.objects.all().order_by('-created_at')
    serializer_class = ShortenedURLSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "click_count"]
    search_fields = ["original_url", "short_code"]

    def get_queryset(self):
        """
        Custom queryset to allow filtering by click count.
        Example: ?min_clicks=10
        """
        queryset = super().get_queryset()
        min_clicks = self.request.query_params.get("min_clicks")

        if min_clicks:
            queryset = queryset.filter(click_count__gte=min_clicks)

        return queryset

    def list(self, request, *args, **kwargs):
        """
        Custom response format.
        """
        queryset = self.get_queryset()
        total_urls = queryset.count()
        most_clicked = queryset.order_by("-click_count").first()

        response_data = {
            "total_urls": total_urls,
            "most_clicked": {
                "short_code": most_clicked.short_code if most_clicked else None,
                "click_count": most_clicked.click_count if most_clicked else None,
            },
            "urls": ShortenedURLSerializer(
                queryset, many=True
            ).data,  # Serialized URL list
        }

        return Response(response_data)

    def retrieve(self, request, short_code=None):
        """
        Redirects a short URL to the original URL and updates the click count.
        """
        url = get_object_or_404(ShortenedURL, short_code=short_code)
        url.click_count += 1
        url.save()
        return redirect(url.original_url)


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
