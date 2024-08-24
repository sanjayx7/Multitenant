from django.contrib import admin
from .models import Client, Domain
from django.db import connection

class ClientAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_add_permission(self, request):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def get_model_perms(self, request):
        """
        Return empty permissions for non-superusers or if the schema is not public,
        hiding the model from those users entirely.
        """
        if request.user.is_superuser and connection.schema_name == 'public':
            return super().get_model_perms(request)
        return {}

class DomainAdmin(admin.ModelAdmin):
    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_add_permission(self, request):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser and connection.schema_name == 'public'

    def get_model_perms(self, request):
        if request.user.is_superuser and connection.schema_name == 'public':
            return super().get_model_perms(request)
        return {}

admin.site.register(Client, ClientAdmin)
admin.site.register(Domain, DomainAdmin)
