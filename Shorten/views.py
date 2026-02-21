from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import ShortenedURL
from .serializers import ShortenedURLSerializer


def _get_client_ip(request):
    forwarded = request.META.get("HTTP_X_FORWARDED_FOR")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.META.get("REMOTE_ADDR")


class URLShortenerViewSet(viewsets.ModelViewSet):
    """List, retrieve, update, and delete shortened URLs with filtering and ordering."""

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["created_at", "click_count"]
    search_fields = ["original_url", "short_code"]

    def get_queryset(self):
        queryset = super().get_queryset()
        min_clicks = self.request.query_params.get("min_clicks")
        if min_clicks:
            queryset = queryset.filter(click_count__gte=min_clicks)
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        total_urls = queryset.count()
        most_clicked = queryset.order_by("-click_count").first()

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
        else:
            serializer = self.get_serializer(queryset, many=True)

        return Response(
            {
                "total_urls": total_urls,
                "most_clicked": {
                    "short_code": most_clicked.short_code if most_clicked else None,
                    "click_count": most_clicked.click_count if most_clicked else 0,
                },
                "urls": serializer.data,
            }
        )


class CreateShortURL(generics.CreateAPIView):
    """Create a new shortened URL."""

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer

    def perform_create(self, serializer):
        serializer.save(ip_address=_get_client_ip(self.request))


class RedirectShortURL(APIView):
    """Redirect a short URL to the original URL."""

    def get(self, request, short_code):
        url = get_object_or_404(ShortenedURL, short_code=short_code)
        ShortenedURL.objects.filter(pk=url.pk).update(click_count=F("click_count") + 1)
        return redirect(url.original_url)


class URLAnalytics(generics.RetrieveAPIView):
    """Retrieve analytics for a shortened URL."""

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = "short_code"
