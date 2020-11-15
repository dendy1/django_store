from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError
from django.test import TestCase

from web_store.models import Seller


class SellerModelCreationTests(TestCase):

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

    def test_valid_user_creation(self):
        seller = Seller.objects.create(
            username='borodin_a_o',
            password='password',
            email='borodin_a_o@sc.vsu.ru',
            phone='+7-952-952-52-38',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich'
        )

        self.assertEqual(seller.username, 'borodin_a_o')
        self.assertNotEqual(seller.password, 'password')
        self.assertTrue(check_password('password', seller.password))
        self.assertEqual(seller.email, 'borodin_a_o@sc.vsu.ru')
        self.assertEqual(seller.phone, '+7-952-952-52-38')
        self.assertEqual(seller.first_name, 'Andrei')
        self.assertEqual(seller.last_name, 'Borodin')
        self.assertEqual(seller.middle_name, 'Olegovich')

    def test_blank_username_data(self):
        self.assertRaisesMessage(ValidationError, 'The username can\'t be blank', Seller.objects.create_user,
                                 username='', password='password', email='example@gmail.com', phone='+7-952-952-52-38')

    def test_email_invalid_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Only alphanumeric characters are allowed',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example_тест@gmail.com',
                                 phone='+7-952-952-52-38'
                                 )

    def test_invalid_email_more_50_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 50 characters',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='a' * 60 + '@gmail.com',
                                 phone='+7-952-952-52-38'
                                 )

    def test_invalid_email_format(self):
        self.assertRaisesMessage(ValidationError, 'Enter a valid email address', Seller.objects.create_user,
                                 username='username', password='password', email='exapmle.gmail.com',
                                 phone='+7-952-952-52-38'
                                 )

    def test_username_invalid_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Only alphanumeric characters are allowed.',
                                 Seller.objects.create_user,
                                 username='username_тест', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38'
                                 )

    def test_invalid_username_more_150_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 150 characters',
                                 Seller.objects.create_user,
                                 username='u' * 160, password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38'
                                 )

    def test_invalid_password_less_8_symbols(self):
        self.assertRaisesMessage(ValidationError, 'The minimum password length is 8', Seller.objects.create_user,
                                 username='username',
                                 password='pass', email='example@gmail.com',
                                 phone='+7-952-952-52-38')

    def test_invalid_first_name_more_150_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 150 characters',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', first_name='Andrei' + 'a' * 150
                                 )

    def test_invalid_first_name_invalid_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Only alphanumeric characters are allowed',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', first_name='Andrei$%#^'
                                 )

    def test_invalid_last_name_more_150_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 150 characters',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', last_name='Borodin' + 'a' * 150
                                 )

    def test_invalid_last_name_invalid_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Only alphanumeric characters are allowed',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', last_name='Borodin%#^'
                                 )

    def test_invalid_middle_name_more_150_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Ensure this value has at most 150 characters',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', middle_name='Olegovich' + 'a' * 150
                                 )

    def test_invalid_middle_name_invalid_symbols(self):
        self.assertRaisesMessage(ValidationError, 'Only alphanumeric characters are allowed',
                                 Seller.objects.create_user,
                                 username='username', password='password', email='example@gmail.com',
                                 phone='+7-952-952-52-38', middle_name='Olegovich%#^'
                                 )

    def test_username_is_already_in_use(self):
        valid_user = Seller(username='username', password='password', email='example@gmail.com',
                            phone='+7-952-952-52-38')
        valid_user.save()

        self.assertRaisesMessage(ValidationError, 'User with this Username already exists', Seller.objects.create_user,
                                 username='username', password='password', email='example_new@gmail.com',
                                 phone='+7-908-952-52-38'
                                 )

    def test_email_is_already_in_use(self):
        valid_user = Seller(username='username', password='password', email='example@gmail.com',
                            phone='+7-952-952-52-38')
        valid_user.save()

        self.assertRaisesMessage(ValidationError, 'User with this Email already exists', Seller.objects.create_user,
                                 username='username2', password='password', email='example@gmail.com',
                                 phone='+7-908-952-52-38'
                                 )
