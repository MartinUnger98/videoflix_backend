from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status

class ActivationTests(APITestCase):
    def test_activate_user_success(self):
        user = User.objects.create_user(
            username='inactive',
            email='inactive@example.com',
            password='secret',
            is_active=False
        )
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        url = reverse('activate-user', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_activate_user_invalid_token(self):
        user = User.objects.create_user(username='inactive2', email='x@x.com', password='pw', is_active=False)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = "invalid-token"
        url = reverse('activate-user', kwargs={'uidb64': uid, 'token': token})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
