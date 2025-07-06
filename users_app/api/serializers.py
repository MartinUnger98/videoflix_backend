from django.contrib.auth.models import User
from rest_framework.serializers import ValidationError, CharField, EmailField, ModelSerializer, Serializer
import re
from django.contrib.auth import authenticate
import uuid
from django.db import IntegrityError

class RegisterSerializer(ModelSerializer):
    """
    Handles user registration logic using Django's built-in User model.
    """
    password = CharField(write_only=True)
    email = EmailField(required=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def validate_email(self, value):
        """
        Ensures email is unique before allowing registration.
        """
        if User.objects.filter(email=value).exists():
            raise ValidationError("This email already exists.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        username_raw = email.split('@')[0]
        parts = re.split(r"[.\-_:\\/]", username_raw)
        base_username = " ".join(part.capitalize() for part in parts if part.strip())

        for _ in range(5):
            unique_username = f"{base_username} {str(uuid.uuid4())[:8]}"
            if not User.objects.filter(username=unique_username).exists():
                try:
                    user = User.objects.create_user(
                        username=unique_username,
                        email=email,
                        password=validated_data['password'],
                        is_active=False
                    )
                    return user
                except IntegrityError:
                    continue

        raise ValidationError("Could not generate a unique username. Please try again.")
    
class EmailAuthTokenSerializer(Serializer):
    """
    Authenticates a user using email and password.
    """
    email = EmailField()
    password = CharField()

    def validate(self, attrs):
        """
        Validates email and password, returns the authenticated user.
        """
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
