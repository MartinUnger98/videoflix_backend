from rest_framework.routers import DefaultRouter
from genres_app.api.views import GenreViewSet

from django.urls import path, include

router = DefaultRouter()
router.register(r'genres', GenreViewSet, basename='genre')

urlpatterns = [
    path('', include(router.urls)),
]
