from django.test import TestCase

from web_store.models import Seller, Sale


class SaleModelTests(TestCase):

    def setUp(self) -> None:
        self.seller = Seller.objects.create(username='some_user')
        self.sale = Sale.objects.create(title="Sale Title", body='Sale Body', price=3000, author=self.seller)

    def test_get_absolute_url(self):
        self.assertIsNotNone(self.sale.get_absolute_url())

    def test_get_update_url(self):
        self.assertIsNotNone(self.sale.get_update_url())

    def test_get_delete_url(self):
        self.assertIsNotNone(self.sale.get_delete_url())

    def test_get_create_url(self):
        self.assertIsNotNone(Sale.get_create_url())