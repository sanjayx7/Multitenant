# Tenants/customer/tasks.py

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from tenant_schemas_celery.task import TenantTask
from Tenants.celery import app
import logging

logger = logging.getLogger(__name__)

@app.task(base=TenantTask, bind=True)
def send_welcome_email(self, user_email, username, tenant_name):
    subject = f'Welcome Back to {tenant_name} Admin Panel!'
    message = f"""Hello {username},

Welcome back to the {tenant_name} admin panel. We are glad to see you again!

If you did not initiate this login, please contact our support team immediately.

Best regards,
The {tenant_name} Team"""
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user_email]

    try:
        send_mail(subject, message, from_email, recipient_list, fail_silently=False)
        logger.info(f"Welcome email sent successfully to {user_email} for tenant {tenant_name}")
        return f"Welcome email sent successfully to {user_email}"
    except Exception as e:
        logger.error(f"Failed to send welcome email to {user_email}: {str(e)}")
        return f"Failed to send welcome email to {user_email}: {str(e)}"

@app.task(base=TenantTask, bind=True)
def process_customer_data(self, customer_id):
    # This is an example task for processing customer data
    try:
        # Simulating some processing
        logger.info(f"Processing data for customer {customer_id}")
        # Add your actual processing logic here
        return f"Data processed successfully for customer {customer_id}"
    except Exception as e:
        logger.error(f"Failed to process data for customer {customer_id}: {str(e)}")
        return f"Failed to process data for customer {customer_id}: {str(e)}"

@app.task(base=TenantTask, bind=True)
def update_shop_inventory(self, shop_id):
    # This is an example task for updating shop inventory
    try:
        # Simulating inventory update
        logger.info(f"Updating inventory for shop {shop_id}")
        # Add your actual inventory update logic here
        return f"Inventory updated successfully for shop {shop_id}"
    except Exception as e:
        logger.error(f"Failed to update inventory for shop {shop_id}: {str(e)}")
        return f"Failed to update inventory for shop {shop_id}: {str(e)}"