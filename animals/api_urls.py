from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet)

urlpatterns = [
    path('api/animals/', views.AnimalViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('api/animals/<int:pk>/', views.AnimalViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'})),
    path('api/animals/<int:animal_id>/procedures/', views.AnimalProceduresView.as_view(), name='animal-procedures-api'),
]

urlpatterns += router.urls
