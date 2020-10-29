import re

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SellerManager(BaseUserManager):

    def create_user(self, username, email, password, phone, **extra_fields):

        alphanumeric_pattern = '[0-9a-zA-Z_@+.-]*'
        phone_pattern = '[0-9+-]*'

        if not username:
            raise ValueError(_('The Username must be set'))

        if not re.match(alphanumeric_pattern, username):
            raise ValidationError('Only alphanumeric characters are allowed.')

        if not email:
            raise ValueError(_('The Email must be set'))

        if not password:
            raise ValueError(_('The Password must be set'))

        if not phone:
            raise ValueError(_('The Phone must be set'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user