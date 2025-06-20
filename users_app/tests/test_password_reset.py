from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator

class PasswordResetTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='reset',
            email='reset@example.com',
            password='resetpass',
            is_active=True
        )
        self.url = reverse('password-reset-request')

    def test_password_reset_request(self):
        response = self.client.post(self.url, {'email': 'reset@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_password_reset_request_invalid_email(self):
        response = self.client.post(self.url, {'email': 'invalid@example.com'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_password_reset_complete(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)
        url = reverse('password-reset-complete')
        response = self.client.post(url, {
            'uidb64': uid,
            'token': token,
            'new_password': 'NeuesPasswort123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NeuesPasswort123'))
