from django.apps import AppConfig


class createDefaultSuperuserConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'create_default_superuser'
