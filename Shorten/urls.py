from django.urls import path
from .views import CreateShortURL, RedirectShortURL, URLAnalytics

urlpatterns = [
    path("shorten/", CreateShortURL.as_view(), name="shorten_url"),
    path("<str:short_code>/", RedirectShortURL.as_view(), name="redirect_url"),
    path("analytics/<str:short_code>/", URLAnalytics.as_view(), name="url_analytics"),
]