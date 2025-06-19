from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet, basename='animal')

urlpatterns = [
    path('', include(router.urls)),
    path('api/animals/', views.AnimalListAPIView.as_view(), name='api_animal_list'),
    path('api/animals/<int:pk>/', views.AnimalDetailAPIView.as_view(), name='api_animal_detail'),
    path('api/animals/<int:pk>/procedures/', views.ProcedureListCreateAPIView.as_view(), name='api_procedure_list'),
    path('api/animals/<int:animal_pk>/procedures/<int:pk>/', views.ProcedureDetailAPIView.as_view(),
         name='api_procedure_detail'),
]