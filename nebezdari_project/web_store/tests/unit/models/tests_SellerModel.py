from django.core.exceptions import ValidationError
from django.test import TestCase

from web_store.models import Seller, Sale, Category

# Добавить тесты на правильность валидации при создании / сохранении в БД
class SellerModelTests(TestCase):

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

    def test_string_representation(self):
        seller = Seller(
            username='borodin_a_o',
            password='password',
            email='borodin_a_o@sc.vsu.ru',
            phone='+7-952-952-52-38',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich'
        )
        self.assertEqual(str(seller), 'Borodin Andrei Olegovich [borodin_a_o, borodin_a_o@sc.vsu.ru, +7-952-952-52-38]')

    def test_get_full_name(self):
        seller = Seller(
            username='borodin_a_o',
            password='password',
            email='borodin_a_o@sc.vsu.ru',
            phone='+7-952-952-52-38',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich'
        )
        self.assertEqual(str(seller.get_full_name()), 'Borodin Andrei Olegovich')

    def test_get_absolute_url(self):
        seller = Seller.objects.create_user(
            username='borodin_a_o',
            password='password',
            email='borodin_a_o@sc.vsu.ru',
            phone='+7-952-952-52-38',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich'
        )

        self.assertIsNotNone(seller.get_absolute_url())

    def test_get_sales_list(self):
        categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]

        seller = Seller.objects.create_user(
            username='borodin_a_o',
            password='password',
            email='example@gmail.com',
            phone='+7-952-952-52-38',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich'
        )

        sale1 = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=categories[0], author=seller)
        sale2 = Sale.objects.create(title='2-title', body='2-body', photo='', price=2000, category=categories[1], author=seller)

        self.assertIsNotNone(seller.get_sales_list())
        self.assertEqual(len(seller.get_sales_list()), Sale.objects.filter(author__email=seller.email).count())

    def test_valid_data(self):
        valid_user = Seller(
            username = 'borodin_a_o',
            password = 'password',
            email = 'example@gmail.com',
            phone = '+7-952-952-52-38',
            first_name = 'Andrei',
            last_name = 'Borodin',
            middle_name = 'Olegovich'
        )

        self.assertEqual(valid_user.username, 'borodin_a_o')
        self.assertEqual(valid_user.password, 'password')
        self.assertEqual(valid_user.email, 'example@gmail.com')
        self.assertEqual(valid_user.phone, '+7-952-952-52-38')
        self.assertEqual(valid_user.first_name, 'Andrei')
        self.assertEqual(valid_user.last_name, 'Borodin')
        self.assertEqual(valid_user.middle_name, 'Olegovich')

    def test_blank_username_data(self):
        invalid_user = Seller(username='', password='password', email='example@gmail.com', phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_email_invalid_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example_тест@gmail.com', phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_email_more_50_symbols(self):
        invalid_user = Seller(username='username', password='password', email='a' * 60 + '@gmail.com', phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_email_format(self):
        invalid_user = Seller(username='username', password='password', email='exapmle.gmail.com',
                              phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_username_invalid_symbols(self):
        invalid_user = Seller(username='username_тест', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_username_more_150_symbols(self):
        invalid_user = Seller(username='u' * 160, password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_password_invalid_symbols(self):
        # invalid_user = Seller(username='username', password='password_тест', email='example@gmail.com',
        #                       phone='+7-952-952-52-38')

        self.assertRaises(ValidationError, Seller.objects.create_user, username='username', password='password_тест', email='example@gmail.com',
                          phone='+7-952-952-52-38')
        # self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_password_less_8_symbols(self):
        # invalid_user = Seller(username='username', password='pass', email='example@gmail.com',
        #                       phone='+7-952-952-52-38')
        self.assertRaises(ValidationError, Seller.objects.create_user, username='username', password='pass', email='example@gmail.com',
                              phone='+7-952-952-52-38')
        # self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_first_name_more_150_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', first_name='Andrei' + 'a' * 150)
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_first_name_invalid_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', first_name='Andrei$%#^')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_last_name_more_150_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', last_name='Borodin' + 'a' * 150)
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_last_name_invalid_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', last_name='Borodin%#^')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_middle_name_more_150_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', first_name='Olegovich' + 'a' * 150)
        self.assertRaises(ValidationError, invalid_user.save)

    def test_invalid_middle_name_invalid_symbols(self):
        invalid_user = Seller(username='username', password='password', email='example@gmail.com',
                              phone='+7-952-952-52-38', first_name='Olegovich%#^')
        self.assertRaises(ValidationError, invalid_user.save)

    def test_username_is_already_in_use(self):
        valid_user = Seller(username='username', password='password', email='example@gmail.com', phone='+7-952-952-52-38')
        valid_user.save()
        duplicate_user = Seller(username='username', password='password', email='example_new@gmail.com', phone='+7-908-952-52-38')
        self.assertRaises(ValidationError, duplicate_user.save)

    def test_email_is_already_in_use(self):
        valid_user = Seller(username='username', password='password', email='example@gmail.com', phone='+7-952-952-52-38')
        valid_user.save()
        duplicate_user = Seller(username='username2', password='password', email='example@gmail.com', phone='+7-908-952-52-38')
        self.assertRaises(ValidationError, duplicate_user.save)