from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("main.api_urls")),  # Endpoint REST API Django REST Framework
    path("", include("main.urls")),              # Halaman Web HTML
]