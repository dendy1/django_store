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


    @classmethod
    def setUpClass(cls) -> None:
        cls.seller = Seller.objects.create_user(
            username='borodin_a_o',
            email='borodin_a_o@sc.vsu.ru',
            password='password',
            first_name='Andrei',
            last_name='Borodin',
            middle_name='Olegovich',
            phone='+7-952-952-52-38'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.seller), 'Borodin Andrei Olegovich [borodin_a_o, borodin_a_o@sc.vsu.ru, +7-952-952-52-38]')

    def test_get_full_name(self):
        self.assertEqual(str(self.seller.get_full_name()), 'Borodin Andrei Olegovich')

    def test_get_absolute_url(self):
        self.assertIsNotNone(self.seller.get_absolute_url())

    def test_get_get_sales_list(self):
        categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]

        sale1 = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=categories[0], author=self.seller)
        sale2 = Sale.objects.create(title='2-title', body='2-body', photo='', price=2000, category=categories[1], author=self.seller)

        self.assertIsNotNone(self.seller.get_sales_list())
        self.assertEqual(len(self.seller.get_sales_list()), Sale.objects.filter(author__email=self.seller.email).count())


    def test_valid_data(self):
        valid_user = Seller.objects.create(self.seller_valid_data)

        self.assertEqual(valid_user.email, self.seller_valid_data['email'])
        self.assertEqual(valid_user.username, self.seller_valid_data['username'])
        self.assertEqual(valid_user.password, self.seller_valid_data['password'])
        self.assertEqual(valid_user.first_name, self.seller_valid_data['first_name'])
        self.assertEqual(valid_user.last_name, self.seller_valid_data['last_name'])
        self.assertEqual(valid_user.middle_name, self.seller_valid_data['middle_name'])
        self.assertEqual(valid_user.phone, self.seller_valid_data['phone'])

    def test_blank_username_data(self):
        blank_user = Seller.objects.create(
            username='', password='password', email='example@gmail.com', phone='+7-952-952-52-38'
        )

        self.assertFalse(blank_user)

    # def test_email_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('email', 'borodin_андрей@gmail.com')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_email_more_50_symbols(self):
    #     invalid_form = self.__get_invalid_form('email', 'a' * 50 + '@gmail.com')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_email_format(self):
    #     invalid_form = self.__get_invalid_form('email', 'borodin_a_o.gmail.com')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_username_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('username', 'username_тест')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_username_more_150_symbols(self):
    #     invalid_form = self.__get_invalid_form('username', 'a' * 160)
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_password_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('password', 'password_тест')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_password_less_8_symbols(self):
    #     invalid_form = self.__get_invalid_form('password', 'pass')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_first_name_more_150_symbols(self):
    #     invalid_form = self.__get_invalid_form('first_name', 'f' * 160)
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_first_name_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('first_name', 'Andrei^$%')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_last_name_more_150_symbols(self):
    #     invalid_form = self.__get_invalid_form('last_name', 'l' * 160)
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_first_last_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('last_name', 'Borodin@#$')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_invalid_middle_name_more_150_symbols(self):
    #     invalid_form = self.__get_invalid_form('middle_name', 'm' * 160)
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_first_middle_invalid_symbols(self):
    #     invalid_form = self.__get_invalid_form('middle_name', 'Olegovich^!@#')
    #     self.assertFalse(invalid_form.is_valid())
    #
    # def test_username_is_already_in_use(self):
    #     self.seller = Seller.objects.create_user(
    #         username='example',
    #         password='secret',
    #         email='example@gmail.com'
    #     )
    #
    #     invalid_form = self.__get_invalid_form('username', 'example')
    #     self.assertFalse(invalid_form.is_valid())
    #     self.assertEqual(invalid_form.errors, {
    #         'username': ['This username is already in use.']
    #     })
    #
    # def test_email_is_already_in_use(self):
    #     self.seller = Seller.objects.create_user(
    #         username='example',
    #         password='secret',
    #         email='example@gmail.com'
    #     )
    #
    #     invalid_form = self.__get_invalid_form('email', 'example@gmail.com')
    #     self.assertFalse(invalid_form.is_valid())
    #     self.assertEqual(invalid_form.errors, {
    #         'email': ['This email address is already in use.']
    #     })
    #
    # def __get_invalid_form(self, key, value):
    #     invalid_username_data = copy.deepcopy(self.seller_valid_data)
    #     invalid_username_data[key] = value
    #     return RegisterForm(invalid_username_data)