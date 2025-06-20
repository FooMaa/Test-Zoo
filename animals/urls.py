from django.urls import path
from .admin import admin_site
from . import views


urlpatterns = [
    path('', views.AnimalListView.as_view(), name='animal-list'),
    path('<int:pk>/', views.AnimalDetailView.as_view(), name='animal'),
    path('create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal-update'),
    path('<int:pk>/add_procedure/', views.ProcedureCreateView.as_view(), name='add-procedure'),
    path('admin/', admin_site.urls),
]
