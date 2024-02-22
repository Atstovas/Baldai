from django.apps import AppConfig


class BaldaiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'baldai'

    def ready(self):
        from .signals import create_profile, save_profile