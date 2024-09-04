from django.contrib import admin

# settings file set by os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local") in manage.py
from django.conf import settings
from django.urls import path

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
]
