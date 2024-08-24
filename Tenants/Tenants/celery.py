# Tenants/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
from tenant_schemas_celery.app import CeleryApp as TenantAwareCeleryApp

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Tenants.settings')

app = Celery('DjangoTenants')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')



# Use a string here instead of the actual settings object to avoid circular imports
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# Configure Celery to use Redis as the broker and result backend
app.conf.broker_url = 'redis://localhost:6379/0'
app.conf.result_backend = 'redis://localhost:6379/0'

# Optional: Configure the default queue
#app.conf.task_default_queue = 'default'

# Optional: Set the timezone for scheduled tasks
#app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')