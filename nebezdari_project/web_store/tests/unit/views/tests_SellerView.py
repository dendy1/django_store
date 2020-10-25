from django_webtest import WebTest

from web_store.models import Seller, Category, Sale


class SellerViewTests(WebTest):
    def setUp(self):
        self.seller = Seller.objects.create_user(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale1 = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=self.categories[0], author=self.seller)
        self.sale2 = Sale.objects.create(title='2-title', body='2-body', photo='', price=2000, category=self.categories[1], author=self.seller)

    def test_basic_view(self):
        response = self.client.get(self.seller.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_sale_list_on_seller_guest_page(self):
        response = self.client.get(self.seller.get_absolute_url())

        for sale in self.seller.get_sales_list():
            self.assertContains(response, sale.title)
            self.assertContains(response, sale.category)

    def test_sale_list_on_seller_auth_page(self):
        logged = self.client.login(username='borodin_a_o', password='password')
        self.assertTrue(logged, True)

        response = self.client.get(self.seller.get_absolute_url())
        for sale in self.seller.get_sales_list():
            self.assertContains(response, sale.title)
            self.assertContains(response, sale.category)
            self.assertIn(sale.get_update_url(), response.content.decode())
            self.assertIn(sale.get_delete_url(), response.content.decode())