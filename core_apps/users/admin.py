from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .forms import UserChangeForm, UserCreationForm

User = get_user_model()


# Docs here: https://docs.djangoproject.com/en/5.1/topics/auth/customizing/#custom-users-and-django-contrib-admin
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = [
        "pkid",
        "id",
        "email",
        "first_name",
        "last_name",
        "username",
        "is_superuser",
    ]
    list_display_links = ["pkid", "id", "email", "username"]
    search_fields = ["email", "first_name", "last_name", "username"]
    ordering = ["pkid"]

    # for editing users
    fieldsets = (
        (_("Login Credentials"), {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "username")}),
        (
            _("Permissions and Groups"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important Dates"), {"fields": ("last_login", "date_joined")}),
    )
    # for adding users
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
