from django.apps import AppConfig
from django.db.models.signals import post_migrate

class JudgeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'judge'
    def ready(self):
        from .models import create_default_group
        post_migrate.connect(create_default_group, sender=self)