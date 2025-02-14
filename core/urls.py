from django.urls import path, include

urlpatterns = [
    path("qr/", include("QR.urls")),
    path("", include("Shorten.urls")),
    path("auth/", include("Auth.urls"))
]
