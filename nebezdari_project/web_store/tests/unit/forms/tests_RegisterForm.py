import copy
from django.test import TestCase
from web_store.forms import RegisterForm
from web_store.models import Seller


class RegisterFormTests(TestCase):

    def setUp(self) -> None:
        self.seller_valid_data = {
            'email': 'borodin_a_o@sc.vsu.ru',
            'username': 'borodin_a_o',
            'password': 'password',
            'first_name': 'Andrei',
            'last_name': 'Borodin',
            'middle_name': 'Olegovich',
            'phone': '+7-952-952-52-38'
        }

    def test_init(self):
        RegisterForm(self.seller_valid_data)

    def test_valid_data(self):
        valid_form = RegisterForm(self.seller_valid_data)
        self.assertTrue(valid_form.is_valid())

        seller = valid_form.save()

        self.assertEqual(seller.email, self.seller_valid_data['email'])
        self.assertEqual(seller.username, self.seller_valid_data['username'])
        self.assertEqual(seller.password, self.seller_valid_data['password'])
        self.assertEqual(seller.first_name, self.seller_valid_data['first_name'])
        self.assertEqual(seller.last_name, self.seller_valid_data['last_name'])
        self.assertEqual(seller.middle_name, self.seller_valid_data['middle_name'])
        self.assertEqual(seller.phone, self.seller_valid_data['phone'])

    def test_blank_data(self):
        register_form = RegisterForm({})
        self.assertFalse(register_form.is_valid())
        self.assertEqual(register_form.errors, {
            'email': ['This field is required.'],
            'username': ['This field is required.'],
            'password': ['This field is required.'],
            'phone': ['This field is required.']
        })

    def test_email_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('email', 'borodin_андрей@gmail.com')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_email_more_50_symbols(self):
        invalid_form = self.__get_invalid_form('email', 'a' * 50 + '@gmail.com')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_email_format(self):
        invalid_form = self.__get_invalid_form('email', 'borodin_a_o.gmail.com')
        self.assertFalse(invalid_form.is_valid())

    def test_username_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('username', 'username_тест')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_username_more_150_symbols(self):
        invalid_form = self.__get_invalid_form('username', 'a' * 160)
        self.assertFalse(invalid_form.is_valid())

    def test_password_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('password', 'password_тест')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_password_less_8_symbols(self):
        invalid_form = self.__get_invalid_form('password', 'pass')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_first_name_more_150_symbols(self):
        invalid_form = self.__get_invalid_form('first_name', 'f' * 160)
        self.assertFalse(invalid_form.is_valid())

    def test_first_name_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('first_name', 'Andrei^$%')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_last_name_more_150_symbols(self):
        invalid_form = self.__get_invalid_form('last_name', 'l' * 160)
        self.assertFalse(invalid_form.is_valid())

    def test_first_last_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('last_name', 'Borodin@#$')
        self.assertFalse(invalid_form.is_valid())

    def test_invalid_middle_name_more_150_symbols(self):
        invalid_form = self.__get_invalid_form('middle_name', 'm' * 160)
        self.assertFalse(invalid_form.is_valid())

    def test_first_middle_invalid_symbols(self):
        invalid_form = self.__get_invalid_form('middle_name', 'Olegovich^!@#')
        self.assertFalse(invalid_form.is_valid())

    def test_username_is_already_in_use(self):
        self.seller = Seller.objects.create_user(
            username='example',
            password='secret',
            email='example@gmail.com',
            phone='+7-952-952-52-38'
        )

        invalid_form = self.__get_invalid_form('username', 'example')
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(invalid_form.errors, {
            'username': ['This username is already in use.']
        })

    def test_email_is_already_in_use(self):
        self.seller = Seller.objects.create_user(
            username='example',
            password='secret',
            email='example@gmail.com',
            phone='+7-952-952-52-38'
        )

        invalid_form = self.__get_invalid_form('email', 'example@gmail.com')
        self.assertFalse(invalid_form.is_valid())
        self.assertEqual(invalid_form.errors, {
            'email': ['This email address is already in use.']
        })

    def __get_invalid_form(self, key, value):
        invalid_username_data = copy.deepcopy(self.seller_valid_data)
        invalid_username_data[key] = value
        return RegisterForm(invalid_username_data)