# Tenants/customer/signals.py

from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django_tenants.utils import get_tenant
from .tasks import send_welcome_email
import logging

logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def trigger_welcome_email(sender, request, user, **kwargs):
    try:
        tenant = get_tenant(request)

        if request.path.startswith('/admin/'):
            send_welcome_email.delay(user.email, user.username, tenant.name)

            logger.info(f"Welcome email task queued for {user.email} for tenant {tenant.name}")
    except Exception as e:
        logger.error(f"Failed to queue welcome email for {user.email}: {str(e)}")