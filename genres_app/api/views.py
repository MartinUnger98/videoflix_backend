from rest_framework import viewsets
from genres_app.models import Genre
from .serializers import GenreSerializer

class GenreViewSet(viewsets.ModelViewSet):
    """
    Provides full CRUD operations for genres.
    Inherits from ModelViewSet, which includes:
    - list, create, retrieve, update, partial_update, destroy
    """
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
