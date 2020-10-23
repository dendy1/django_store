import copy
from unittest import TestCase

from django.contrib.auth.forms import AuthenticationForm

from web_store.models import Seller


class AuthenticationFormTests(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.seller = Seller.objects.create_user(
            email='dendy@sc.vsu.ru',
            username='dendy',
            password='password',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich',
            phone='+7-952-952-52-38',
            is_active=True
        )

        cls.seller_valid_data = {
            'username': 'dendy',
            'password': 'password'
        }

    def test_valid_username_password_combination(self):
         valid_form = AuthenticationForm(data=self.seller_valid_data)
         self.assertTrue(valid_form.is_valid())

    def test_blank_data(self):
        authentication_form = AuthenticationForm(data={})
        self.assertFalse(authentication_form.is_valid())
        self.assertEqual(authentication_form.errors, {
            'username': ['This field is required.'],
            'password': ['This field is required.'],
        })

    def test_username_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('username', 'username_тест')
        self.assertFalse(invalid_form.is_valid())

    def test_password_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('password', 'password_тест')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_password_less_8_symbols(self):
        invalid_form = self.__get_invalid_form('password', 'pass')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_username_password_combination(self):
        invalid_form = self.__get_invalid_form('password', 'example')
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(invalid_form.errors, {
            '__all__': ['Please enter a correct username and password. Note that both fields may be case-sensitive.']
        })

    def __get_invalid_form(self, key, value):
        invalid_username_data = copy.deepcopy(self.seller_valid_data)
        invalid_username_data[key] = value
        return AuthenticationForm(data=invalid_username_data)