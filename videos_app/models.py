from django.db import models
from django.conf import settings
from genres_app.models import Genre


class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')
    thumbnail = models.FileField(upload_to='thumbnails/', blank=True, null=True)
    file_120p = models.FileField(upload_to='videos/120p/', blank=True, null=True)
    file_360p = models.FileField(upload_to='videos/360p/', blank=True, null=True)
    file_720p = models.FileField(upload_to='videos/720p/', blank=True, null=True)
    file_1080p = models.FileField(upload_to='videos/1080p/', blank=True, null=True)
    hls_playlist = models.CharField(max_length=500, blank=True, null=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True, related_name='videos')
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class VideoProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='progress')
    timestamp = models.FloatField(help_text="Time in seconds")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f"{self.user} - {self.video} @ {self.timestamp:.2f}s"
