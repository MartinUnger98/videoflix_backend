from django.apps import AppConfig

class UsersAppConfig(AppConfig):
    """
    Configuration for the users_app.
    Ensures signals are registered when the app is ready.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users_app'

    def ready(self):
        # Import signals to activate them on app initialization
        from . import signals
