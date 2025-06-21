from rest_framework import serializers
from genres_app.models import Genre

class GenreSerializer(serializers.ModelSerializer):
    """
    Serializer for Genre model.
    Converts Genre model instances to JSON and validates input data.
    """
    class Meta:
        model = Genre
        fields = ['id', 'name']
