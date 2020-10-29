from django.test import TestCase
from django.urls import reverse

from web_store.models import Seller, Sale, Category


class SaleModelTests(TestCase):

    def setUp(self) -> None:
        self.seller = Seller.objects.create_user(username='some_user', password='password', email='example@mail.com', phone='+7-952-952-52-38')
        categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale = Sale.objects.create(title="Sale Title", body='Sale Body', price=3000, category=categories[0], author=self.seller)

    def test_get_absolute_url(self):
        self.assertIsNotNone(self.sale.get_absolute_url())

    def test_get_update_url(self):
        self.assertIsNotNone(self.sale.get_update_url())

    def test_get_delete_url(self):
        self.assertIsNotNone(self.sale.get_delete_url())

    def test_get_create_url(self):
        self.assertIsNotNone(reverse('sale_create'))