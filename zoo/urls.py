from django.urls import path, include

from animals.admin import admin_site


urlpatterns = [
    path('', include('animals.urls')),
    path('admin/animals/', admin_site.urls),
    path('api/', include('animals.api_urls')),
]
