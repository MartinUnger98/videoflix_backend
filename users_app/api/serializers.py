from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError, CharField, EmailField, ModelSerializer, Serializer
import re
from django.contrib.auth import authenticate

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
    
class EmailAuthTokenSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                raise ValidationError("Invalid email or password.")

            user = authenticate(username=user.username, password=password)
            if not user:
                raise ValidationError("Invalid email or password.")
        else:
            raise ValidationError("Both email and password are required.")

        attrs["user"] = user
        return attrs
