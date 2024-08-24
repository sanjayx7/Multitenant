from django.apps import AppConfig

class DjangoTenantConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'customer'  # Change this to match your app name

    def ready(self):
        import customer.signals  # Change this import as well