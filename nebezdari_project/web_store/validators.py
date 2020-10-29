import re

from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class AlphaNumericValidator(object):
    def validate(self, password, user=None):
        pattern = re.compile('[0-9a-zA-Z_@+.-]*')
        if not (pattern.match(password)):
            raise ValidationError(_('Only alphanumeric characters are allowed.'))

    def get_help_text(self):
        return ""