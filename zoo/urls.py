from django.urls import path, include

from .admin import admin_site


urlpatterns = [
    path('', include('animals.urls')),
    path('admin/', admin_site.urls),
    path('api/', include('animals.api_urls')),
]
