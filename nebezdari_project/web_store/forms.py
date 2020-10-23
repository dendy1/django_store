from django import forms
from django.core.validators import RegexValidator

from web_store.models import Seller


class RegisterForm(forms.ModelForm):
    alphanumeric_symbols = RegexValidator(r'^[0-9a-zA-Z_@+.-]*$', 'Only alphanumeric characters are allowed.')
    alpha_only = RegexValidator(r'^[a-zA-Zа-яА-Я]*$', 'Only alphanumeric characters are allowed.')
    phone_validator = RegexValidator(r'^[0-9+-]*$')

    username = forms.CharField(max_length=150, required=True, validators=[alphanumeric_symbols])
    password = forms.CharField(min_length=8, required=True, validators=[alphanumeric_symbols], widget=forms.PasswordInput)

    phone = forms.CharField(max_length=30, validators=[phone_validator])

    first_name = forms.CharField(max_length=150, required=False, validators=[alpha_only])
    last_name = forms.CharField(max_length=150, required=False, validators=[alpha_only])
    middle_name = forms.CharField(max_length=150, required=False, validators=[alpha_only])

    def clean_username(self):
        try:
            seller = Seller.objects.get(username__iexact=self.cleaned_data['username'])
        except Seller.DoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError('This username is already in use.')

    def clean_email(self):
        try:
            seller = Seller.objects.get(email__iexact=self.cleaned_data['email'])
        except Seller.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError('This email address is already in use.')

    class Meta:
        model = Seller
        fields = ('email', 'username', 'password', 'phone', 'first_name', 'last_name', 'middle_name')