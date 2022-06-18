from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

from .validators import CustomUsernameValidator


# create custom user by change or/and add fields (Based on Abstract User)
class CustomUser(AbstractUser):

    # add unique to email field
    email = models.EmailField(_("email address"), 
        unique=True,
        error_messages={
            "unique": _("A user with that email already exists."),
        },
    )  

    is_email_verified = models.BooleanField(default=False)

    username_validator = CustomUsernameValidator()

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required field with max 150 characters. Letters, digits and ./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )