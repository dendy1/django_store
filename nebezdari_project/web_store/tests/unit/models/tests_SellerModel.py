from unittest import TestCase

from web_store.models import Seller, Sale, Category


class SellerModelTests(TestCase):

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