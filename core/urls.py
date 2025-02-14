from django.urls import path, include

urlpatterns = [
    path("qr/", include("QR.urls")),
    path("", include("Shorten.urls")),
]
