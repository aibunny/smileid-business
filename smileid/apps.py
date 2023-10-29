from django.apps import AppConfig


class SmileidConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'smileid'
    
    def ready(self):
        from . import tasks 
