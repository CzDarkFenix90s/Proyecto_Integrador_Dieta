from django.apps import AppConfig


class DieteticConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'dietetic'
    verbose_name = 'Consulta Dietética'

    def ready(self):
        import dietetic.signals
