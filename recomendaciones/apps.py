from django.apps import AppConfig
from django.db.models.signals import post_migrate


class RecomendacionesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'recomendaciones'
    def ready(self):
            # Conectar la señal post_migrate al método para crear datos iniciales
            from .signals import create_initial_data
            post_migrate.connect(create_initial_data, sender=self)