from django.urls import path
from django.views.generic import RedirectView

from . import views


urlpatterns = [
    path('', RedirectView.as_view(url='/animals/',  permanent=False)),
    path('admin/', RedirectView.as_view(url='admin/animals/', permanent=True)),

    path('animals/', views.AnimalListView.as_view(), name='animal-list'),
    path('animals/<int:pk>/', views.AnimalDetailView.as_view(), name='animal'),
    path('animals/create/', views.AnimalCreateView.as_view(), name='animal-create'),
    path('animals/<int:pk>/update/', views.AnimalUpdateView.as_view(), name='animal-update'),
    path('animals/<int:pk>/procedures/create', views.ProcedureCreateView.as_view(), name='add-procedure'),
]
