from django.test import TestCase
from videos_app.models import Video
from genres_app.models import Genre
from videos_app.tasks import process_video_file
from django.core.files.uploadedfile import SimpleUploadedFile
import os
from unittest.mock import patch

class VideoTaskTests(TestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="Test")
        self.video = Video.objects.create(
            title="TaskTest",
            description="Testdesc",
            genre=self.genre,
            video_file=SimpleUploadedFile("video.mp4", b"data", content_type="video/mp4")
        )

    @patch("videos_app.tasks.subprocess.run")
    def test_process_video_file_runs(self, mock_run):
        mock_run.return_value = None
        process_video_file(self.video.id)
        self.assertEqual(mock_run.call_count, 6)

    def test_video_post_delete_signal(self):
        video = self.video
        path = video.video_file.path
        self.assertTrue(os.path.exists(path))
        video.delete()
        self.assertFalse(os.path.exists(path))