from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import api_views


router = DefaultRouter()
router.register(r'animals', api_views.AnimalViewSet, basename='animal')

urlpatterns = [
    path('', include(router.urls)),
    path('animals/<int:pk>/procedures/', api_views.ProcedureListCreateAPIView.as_view(), name='api_procedure_list'),
    path('animals/<int:animal_pk>/procedures/<int:pk>/', api_views.ProcedureDetailAPIView.as_view(), name='api_procedure_detail'),
]
