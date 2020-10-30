from unittest.mock import patch

from django.urls import reverse
from django_mock_queries.query import MockSet
from django_webtest import WebTest

from web_store.models import Seller, Category, Sale
from web_store.views.SellerViews import SellerDetail


class SellerViewTests(WebTest):
    def setUp(self):
        self.seller_qs = MockSet(model=Seller)
        self.category_qs = MockSet(model=Category)
        self.sale_qs = MockSet(model=Sale)

        self.seller = self.seller_qs.create(
            username='borodin_a_o',
            email='borodin_a_o@sc.vsu.ru',
            password='password',
            phone='+7-952-952-52-38'
        )

        self.category1 = self.category_qs.create(category_name='Category1')
        self.category2 = self.category_qs.create(category_name='Category2')

        self.sale1 = self.sale_qs.create(
            title='1-title',
            body='1-body',
            photo='',
            price=1000,
            category=self.category1,
            author=self.seller
        )
        self.sale2 = self.sale_qs.create(
            title='2-title',
            body='2-body',
            photo='',
            price=2000,
            category=self.category2,
            author=self.seller
        )

    def test_basic_view(self):
        with patch.object(SellerDetail, 'get_object', return_value=self.seller):
            url = reverse('seller_detail', kwargs={'pk': 1})  # pk can be anything
            response = self.client.get(url)
            self.assertEqual(response.status_code, 200)

    def test_sale_list_on_seller_guest_page(self):
        with patch.object(SellerDetail, 'get_object', return_value=self.seller):
            url = reverse('seller_detail', kwargs={'pk': 1})  # pk can be anything
            response = self.client.get(url)

            for sale in self.seller.get_sales_list():
                self.assertContains(response, sale.title)
                self.assertContains(response, sale.category)

    def test_sale_list_on_seller_auth_page(self):
        with patch.object(SellerDetail, 'get_object', return_value=self.seller):
            url = reverse('seller_detail', kwargs={'pk': 1})  # pk can be anything
            response = self.client.get(url)

            for sale in self.seller.get_sales_list():
                self.assertContains(response, sale.title)
                self.assertContains(response, sale.category)
                self.assertIn(sale.get_update_url(), response.content.decode())
                self.assertIn(sale.get_delete_url(), response.content.decode())