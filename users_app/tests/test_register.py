from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User

class RegisterTests(APITestCase):
    def setUp(self):
        self.url = reverse('register')

    def test_register_success(self):
        response = self.client.post(self.url, {
            'email': 'user@example.com',
            'password': 'Testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='user@example.com').exists())

        user = User.objects.get(email='user@example.com')
        self.assertFalse(user.is_active)
        self.assertTrue(user.username.startswith('User'))

    def test_register_duplicate_email(self):
        User.objects.create_user(username='existing', email='user@example.com', password='secret')
        response = self.client.post(self.url, {
            'email': 'user@example.com',
            'password': 'Testpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
