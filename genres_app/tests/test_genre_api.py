from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from genres_app.models import Genre


class GenreAPITests(APITestCase):
    def setUp(self):
        self.list_url = reverse('genre-list')

    def test_create_genre(self):
        response = self.client.post(self.list_url, {'name': 'Action'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Genre.objects.filter(name='Action').exists())

    def test_list_genres(self):
        Genre.objects.create(name='Comedy')
        Genre.objects.create(name='Drama')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_genre(self):
        genre = Genre.objects.create(name='Sci-Fi')
        detail_url = reverse('genre-detail', args=[genre.id])
        response = self.client.get(detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sci-Fi')

    def test_update_genre(self):
        genre = Genre.objects.create(name='Old')
        detail_url = reverse('genre-detail', args=[genre.id])
        response = self.client.patch(detail_url, {'name': 'New'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        genre.refresh_from_db()
        self.assertEqual(genre.name, 'New')

    def test_delete_genre(self):
        genre = Genre.objects.create(name='ToDelete')
        detail_url = reverse('genre-detail', args=[genre.id])
        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Genre.objects.filter(id=genre.id).exists())
