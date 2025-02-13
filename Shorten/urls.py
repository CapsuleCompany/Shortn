from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CreateShortURL, RedirectShortURL, URLAnalytics, URLShortenerViewSet


router = DefaultRouter()
router.register(r"urls", URLShortenerViewSet, basename="short-url")
urlpatterns = [
    path("", include(router.urls)),  # Includes all `ModelViewSet` routes
    path("shorten/", CreateShortURL.as_view(), name="shorten_url"),
    path("<str:short_code>/", RedirectShortURL.as_view(), name="redirect_url"),
    path("analytics/<str:short_code>/", URLAnalytics.as_view(), name="url_analytics"),
]
