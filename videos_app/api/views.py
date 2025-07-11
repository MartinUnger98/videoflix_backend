from rest_framework import viewsets, permissions
from videos_app.models import Video, VideoProgress
from videos_app.api.serializers import VideoSerializer, VideoProgressSerializer


class VideoViewSet(viewsets.ModelViewSet):
    """
    Public view for listing, retrieving and reading videos.
    Allows unrestricted access (used for public video listing).
    """
    queryset = Video.objects.all()
    serializer_class = VideoSerializer
    permission_classes = [permissions.IsAuthenticated]


class VideoProgressViewSet(viewsets.ModelViewSet):
    """
    Allows authenticated users to track and update their video progress.
    Ensures each user accesses only their own progress entries.
    """
    serializer_class = VideoProgressSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VideoProgress.objects.filter(user=self.request.user)
