from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework import status

class LogoutTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='logout',
            password='logoutpass',
            is_active=True
        )
        self.token = Token.objects.create(user=self.user)
        self.url = reverse('logout')

    def test_logout_success(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
