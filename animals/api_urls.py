from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'animals', views.AnimalViewSet)

urlpatterns = [
    path('animals/<int:animal_id>/procedures/',
         views.AnimalProceduresView.as_view(),
         name='animal-procedures-api'),
]

urlpatterns += router.urls
