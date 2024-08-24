import logging
from django.http import HttpResponseForbidden
from django_tenants.utils import get_tenant_model
from django.utils.deprecation import MiddlewareMixin
from django.core.exceptions import PermissionDenied

logger = logging.getLogger(__name__)

class TenantPermissionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if not request.user.is_authenticated:
            return None

        tenant_model = get_tenant_model()
        try:
            tenant = tenant_model.objects.get(schema_name=request.tenant.schema_name)
        except tenant_model.DoesNotExist:
            return HttpResponseForbidden("Tenant does not exist.")

        user = request.user
        tenant_permissions = set(tenant.get_permissions_list())

        logger.debug(f"User: {user.username}, Tenant: {tenant.name}, Schema: {tenant.schema_name}")
        logger.debug(f"Tenant permissions: {tenant_permissions}")
        logger.debug(f"View function: {view_func.__name__}")
        logger.debug(f"Path: {request.path}")

        # Allow superusers full access in the public schema
        if user.is_superuser and request.tenant.schema_name == 'public':
            return None

        # Always allow access to jsi18n
        if request.path.endswith('/jsi18n/'):
            return None

        # Check if the user is accessing the admin panel
        if request.path.startswith('/admin/'):
            if not user.is_staff:
                raise PermissionDenied("You don't have permission to access the admin panel.")

            # Allow view access for all staff users
            if request.method == 'GET':
                return None

            # Check permissions for admin actions
            if 'add' in request.path:
                if not any(perm.startswith('shop.add_') for perm in tenant_permissions):
                    raise PermissionDenied("Your plan doesn't allow adding items.")
            elif 'delete' in request.path:
                if not any(perm.startswith('shop.delete_') for perm in tenant_permissions):
                    raise PermissionDenied("Your plan doesn't allow deleting items.")
            elif 'change' in request.path:
                if not any(perm.startswith('shop.change_') for perm in tenant_permissions):
                    raise PermissionDenied("Your plan doesn't allow changing items.")

        return None