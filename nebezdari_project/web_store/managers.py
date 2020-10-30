import re

from django.contrib.auth.base_user import BaseUserManager
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _


class SellerManager(BaseUserManager):

    def create(self, username, email, password, phone, **extra_fields):

        alphanumeric_pattern = '[0-9a-zA-Z_@+.-]*'
        phone_pattern = '[0-9+-]*'
        email_pattern = '[0-9a-zA-Z_@+.-]*'
        alpha_only_pattern = '[a-zA-Zа-яА-Я]'

        if not username:
            raise ValidationError(_('The username can\'t be blank.'))

        if not re.match(alphanumeric_pattern, username):
            raise ValidationError('Only alphanumeric characters are allowed.')

        if not email:
            raise ValidationError(_('The email can\'t be blank.'))

        if not re.match(email_pattern, email):
            raise ValidationError('Only english alphanumeric characters are allowed.')

        if not password:
            raise ValidationError(_('The password can\'t be blank.'))

        if not re.match(alphanumeric_pattern, password):
            raise ValidationError('Only alphanumeric characters are allowed.')

        if len(password) < 8:
            raise ValidationError('The minimum password length is 8.')

        if not phone:
            raise ValidationError(_('The phone can\'t be blank.'))

        if not re.match(phone_pattern, phone):
            raise ValidationError('Only numeric characters are allowed.')

        if 'first_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['first_name']):
                raise ValidationError('Only alpha characters are allowed.')

        if 'last_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['last_name']):
                raise ValidationError('Only alpha characters are allowed.')

        if 'middle_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['middle_name']):
                raise ValidationError('Only alpha characters are allowed.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username, email, password, phone, **extra_fields):

        alphanumeric_pattern = '[0-9a-zA-Z_@+.-]*'
        phone_pattern = '[0-9+-]*'
        email_pattern = '[0-9a-zA-Z_@+.-]*'
        alpha_only_pattern = '[a-zA-Zа-яА-Я]'

        if not username:
            raise ValidationError(_('The username can\'t be blank.'))

        if not re.match(alphanumeric_pattern, username):
            raise ValidationError('Only alphanumeric characters are allowed.')

        if not email:
            raise ValidationError(_('The email can\'t be blank.'))

        if not re.match(email_pattern, email):
            raise ValidationError('Only english alphanumeric characters are allowed.')

        if not password:
            raise ValidationError(_('The password can\'t be blank.'))

        if not re.match(alphanumeric_pattern, password):
            raise ValidationError('Only alphanumeric characters are allowed.')

        if len(password) < 8:
            raise ValidationError('The minimum password length is 8.')

        if not phone:
            raise ValidationError(_('The phone can\'t be blank.'))

        if not re.match(phone_pattern, phone):
            raise ValidationError('Only numeric characters are allowed.')

        if 'first_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['first_name']):
                raise ValidationError('Only alpha characters are allowed.')

        if 'last_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['last_name']):
                raise ValidationError('Only alpha characters are allowed.')

        if 'middle_name' in extra_fields:
            if not re.match(alpha_only_pattern, extra_fields['middle_name']):
                raise ValidationError('Only alpha characters are allowed.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save()
        return user