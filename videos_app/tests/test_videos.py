from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from videos_app.models import Video
from genres_app.models import Genre
from django.contrib.auth.models import User


class VideoAPITests(APITestCase):
    def setUp(self):
        self.genre = Genre.objects.create(name="TestGenre")
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.client.force_authenticate(user=self.user)

        self.url = reverse('video-list')

    def get_test_video_file(self):
        return SimpleUploadedFile("test_video.mp4", b"fakevideocontent", content_type="video/mp4")

    def test_create_video(self):
        data = {
            'title': 'Test Video',
            'description': 'Kurzbeschreibung',
            'genre': self.genre.id,
            'video_file': self.get_test_video_file()
        }
        response = self.client.post(self.url, data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Video.objects.filter(title='Test Video').exists())
        self.assertEqual(Video.objects.count(), 1)

    def test_list_videos(self):
        Video.objects.create(
            title='Video 1',
            description='Beschreibung',
            video_file=self.get_test_video_file(),
            genre=self.genre
        )
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_video_detail(self):
        video = Video.objects.create(
            title='Detail Video',
            description='Beschreibung',
            video_file=self.get_test_video_file(),
            genre=self.genre
        )
        detail_url = reverse('video-detail', args=[video.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Detail Video')
        
    def test_video_progress_list_authenticated(self):
        user = User.objects.create_user(username='test', password='pass')
        self.client.force_authenticate(user=user)
        url = reverse('video-progress-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        
    def test_video_str_method(self):
        video = Video.objects.create(
            title='String Test',
            description='Test',
            video_file=self.get_test_video_file(),
            genre=self.genre
        )
        self.assertEqual(str(video), 'String Test')
    
    def test_video_progress_str_method(self):
        video = Video.objects.create(
            title='ForProgress',
            description='Test',
            video_file=self.get_test_video_file(),
            genre=self.genre
        )
        progress = video.progress.create(user=self.user, timestamp=12.3)  # self.user statt neuen User
        self.assertIn("testuser", str(progress))