from django.apps import AppConfig


class CadastramentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastramento'


from django.apps import AppConfig

class CadastramentoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'cadastramento'

    def ready(self):
        import cadastramento.signals
