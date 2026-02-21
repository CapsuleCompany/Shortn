from django.conf import settings
from django.core.cache import cache
from django.db.models import F
from django.shortcuts import get_object_or_404, redirect
from rest_framework import filters, generics, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from core.logging import event_logger

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
        instance = serializer.save(ip_address=_get_client_ip(self.request))
        user = None
        if self.request.user and self.request.user.is_authenticated:
            user = self.request.user.username
        event_logger.url_created(
            short_code=instance.short_code,
            original_url=instance.original_url,
            ip_address=instance.ip_address,
            user=user,
        )


class RedirectShortURL(APIView):
    """Redirect a short URL to the original URL.

    Caches the short_code -> original_url mapping to avoid DB hits on repeat visits.
    """

    def get(self, request, short_code):
        cache_key = f"shortn:redirect:{short_code}"
        original_url = cache.get(cache_key)

        if original_url is None:
            url = get_object_or_404(ShortenedURL, short_code=short_code)
            original_url = url.original_url
            cache.set(cache_key, original_url, settings.REDIRECT_CACHE_TTL)
            pk = url.pk
            cached = False
        else:
            # Still need the pk for the click count update
            pk = (
                ShortenedURL.objects.filter(short_code=short_code)
                .values_list("pk", flat=True)
                .first()
            )
            cached = True

        ShortenedURL.objects.filter(pk=pk).update(click_count=F("click_count") + 1)
        event_logger.url_redirected(short_code=short_code, cached=cached)
        return redirect(original_url)


class URLAnalytics(generics.RetrieveAPIView):
    """Retrieve analytics for a shortened URL.

    Responses are cached briefly to reduce DB load under heavy polling.
    """

    queryset = ShortenedURL.objects.all()
    serializer_class = ShortenedURLSerializer
    lookup_field = "short_code"

    def retrieve(self, request, *args, **kwargs):
        short_code = self.kwargs["short_code"]
        cache_key = f"shortn:analytics:{short_code}"
        data = cache.get(cache_key)

        cached = data is not None
        if not cached:
            instance = self.get_object()
            serializer = self.get_serializer(instance)
            data = serializer.data
            cache.set(cache_key, data, settings.ANALYTICS_CACHE_TTL)

        event_logger.url_analytics_viewed(short_code=short_code, cached=cached)
        return Response(data)
