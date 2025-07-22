from django.apps import AppConfig
from django.db.models.signals import post_migrate

class PostlistConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'postlist'
    def ready(self):
        from .models import create_default_group
        post_migrate.connect(create_default_group, sender=self)