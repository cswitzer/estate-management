import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("chase_apartments")

# Read configuration from Django settings
app.config_from_object("django.conf:settings", namespace="CELERY")

# Find all tasks.py in all installed apps
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)
