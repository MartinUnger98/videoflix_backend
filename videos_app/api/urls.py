from rest_framework.routers import DefaultRouter
from videos_app.api.views import VideoViewSet, VideoProgressViewSet
from django.urls import path, include

router = DefaultRouter()
router.register(r'videos', VideoViewSet, basename='video')
router.register(r'progress', VideoProgressViewSet, basename='video-progress')

urlpatterns = [
    path('', include(router.urls)),
]
