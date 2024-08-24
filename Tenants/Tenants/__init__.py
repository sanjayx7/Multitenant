from __future__ import absolute_import, unicode_literals

# Django starts so that shared tasks will use this app.
from .celery import app as celery_app

_all_ =('celery_app',)