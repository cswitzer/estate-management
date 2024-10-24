from django.contrib import admin

# settings file set by os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local") in manage.py
from django.conf import settings
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions


schema_view = get_schema_view(
    openapi.Info(
        title="Chase Apartments API",
        default_version="v1",
        description="API for Chase Apartments",
        contact=openapi.Contact(email="api.imperfect@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v1/auth/", include("djoser.urls")),
    path("api/v1/auth/", include("core_apps.users.urls")),
]

admin.site.site_header = "Chase Apartments Admin"
admin.site.site_title = "Chase Apartments Admin Portal"
admin.site.index_title = "Welcome to Chase Apartments Admin Portal"
