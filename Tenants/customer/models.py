from django_tenants.models import TenantMixin, DomainMixin
from django_tenants.utils import schema_context
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from Tenants.permissions import BASIC_PERMISSIONS, PREMIUM_PERMISSIONS, PROFESSIONAL_PERMISSIONS
from django.db import models
from django_tenants.models import TenantMixin

class Client(TenantMixin):
    name = models.CharField(max_length=100)
    created_on = models.DateField(auto_now_add=True)
    subscription_plan = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('premium', 'Premium'),
            ('professional', 'Professional')
        ],
        default='basic'
    )
    auto_create_schema = True

    def __str__(self):
        return self.name

    def get_permissions_list(self):
        if self.subscription_plan == 'professional':
            return PROFESSIONAL_PERMISSIONS
        elif self.subscription_plan == 'premium':
            return PREMIUM_PERMISSIONS
        else:
            return BASIC_PERMISSIONS



    class Meta:
        permissions = [
            ("can_add_client", "Can add client"),
            ("can_change_client", "Can change client"),
            ("can_delete_client", "Can delete client"),
            ("can_view_client", "Can view client"),
        ]

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new or 'subscription_plan' in kwargs.get('update_fields', []):
            self.update_tenant_permissions()

    def update_tenant_permissions(self):
        with schema_context(self.schema_name):
            print(f"Updating permissions for tenant: {self.name} (schema: {self.schema_name})")

            permissions_list = set(self.get_permissions_list())
            existing_permissions = set(Permission.objects.values_list('codename', flat=True))

            # Remove permissions not in the list
            Permission.objects.exclude(codename__in=permissions_list).delete()

            # Add new permissions
            for permission_codename in permissions_list - existing_permissions:
                parts = permission_codename.split('.')
                if len(parts) != 2:
                    print(f"Skipping invalid permission: {permission_codename}")
                    continue
                app_label, action_model = parts
                action, model = action_model.split('_')
                try:
                    content_type = ContentType.objects.get(app_label=app_label, model=model)
                    permission, created = Permission.objects.get_or_create(
                        codename=action_model,
                        name=f'Can {action} {model}',
                        content_type=content_type
                    )
                    if created:
                        print(f"Created permission: {permission.codename}")
                    else:
                        print(f"Permission already exists: {permission.codename}")
                except ContentType.DoesNotExist:
                    print(f"Skipping permission due to missing content type: {app_label}.{model}")
                except Exception as e:
                    print(f"Error creating permission {permission_codename}: {str(e)}")

            # Verify permissions after update
            final_permissions = Permission.objects.all()
            print(f"Final permissions count: {final_permissions.count()}")
            for perm in final_permissions:
                print(f"- {perm.content_type.app_label}.{perm.codename}")

class Domain(DomainMixin):
    pass