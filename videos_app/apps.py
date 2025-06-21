from django.apps import AppConfig


class VideosAppConfig(AppConfig):
    """
    Configuration for the videos_app.
    Ensures signals are registered when the app is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'videos_app'
    def ready(self):
        # Import signals to activate them on app initialization
        from . import signals
