from django.db import models

class Genre(models.Model):
    """
    Represents a video genre, such as Comedy, Drama, etc.
    The 'name' field must be unique.
    """
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name
