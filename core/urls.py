from django.urls import path, include

urlpatterns = [
       path("", include('Shorten.urls')),
]
