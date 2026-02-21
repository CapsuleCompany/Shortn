from django.urls import include, path
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def health_check(request):
    return Response({"status": "healthy"})


@api_view(["GET"])
def api_info(request):
    return Response(
        {
            "service": "Shortn",
            "version": "1.0.0",
            "endpoints": {
                "shorten": "/shorten/",
                "redirect": "/<short_code>/",
                "urls": "/urls/",
                "analytics": "/analytics/<short_code>/",
                "qr_generate": "/qr/generate/",
                "auth_register": "/auth/register/",
                "auth_login": "/auth/login/",
                "auth_refresh": "/auth/refresh/",
                "health": "/health/",
            },
        }
    )


urlpatterns = [
    path("", api_info, name="api-info"),
    path("health/", health_check, name="health-check"),
    path("qr/", include("QR.urls")),
    path("auth/", include("Auth.urls")),
    path("", include("Shorten.urls")),
]
