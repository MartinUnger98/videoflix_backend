from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError, CharField, EmailField, ModelSerializer
import re

class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username_raw = email.split('@')[0]
        parts = re.split(r"[.\-_:\\/]", username_raw)
        username = " ".join(part.capitalize() for part in parts if part.strip())

        user = User.objects.create_user(
            username=username,
            email=email,
            password=validated_data['password'],
            is_active=False
        )
        return user
