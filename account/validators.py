import re

from django.core import validators
from django.utils.deconstruct import deconstructible
from django.utils.translation import gettext_lazy as _


@deconstructible
class CustomUsernameValidator(validators.RegexValidator):
    """
    A custom username validator without '@' in username for easier determination whether it is an email or a username
    """
    regex = r"^[\w.+-]+\Z"
    message = _(
        "Enter a valid username. This value may contain only English letters, "
        "numbers, and ./+/-/_ characters."
    )
    flags = re.ASCII
