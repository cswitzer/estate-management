import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core import validators
from django.utils.translation import gettext_lazy as _
from core_apps.users.managers import UserManager


class UsernameValidator(validators.RegexValidator):
    regex = r"^[\w.@+-]+\Z"
    message = _(
        "Your username is not valid. A username can only contain letters, numbers, a dot, "
        "@ symbol, + symbol and a hyphen "
    )
    flag = 0


class User(AbstractUser):
    # psuedo primary key
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    username = models.CharField(
        verbose_name=_("Username"),
        max_length=60,
        unique=True,
        validators=[UsernameValidator],
    )
    email = models.EmailField(
        verbose_name=_("Email Address"), unique=True, db_index=True
    )
    first_name = models.CharField(verbose_name=_("First Name"), max_length=60)
    last_name = models.CharField(verbose_name=_("Last Name"), max_length=60)

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"

    # email field already required by above USERNAME_FIELD
    # these are the fields required by createsuperuser command
    REQUIRED_FIELDS = ["username", "first_name", "last_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ["-date_joined"]

    @property
    def get_full_name(self) -> str:
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()
