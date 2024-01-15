import datetime

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


class NoFutureDateValidator:
    """Validate that the date is not in the future"""

    message = _("The date may not be in the future.")
    code = "no_future_date"

    def __init__(self, message=None, code=None):
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

    def __call__(self, value):
        if value > datetime.date.today():
            raise ValidationError(message=self.message, code=self.code, params={'value': value})

