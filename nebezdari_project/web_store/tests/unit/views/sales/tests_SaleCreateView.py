from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller, Category, Sale


class SaleCreateViewTests(WebTest):

    def setUp(self):
        self.seller = Seller.objects.create_user(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, author=self.seller)
        self.sale.categories.add(self.categories[0], self.categories[1])

    def test_create_view(self):
        response = self.client.get(reverse('sale_create'))
        self.assertRedirects(response, reverse('login') + '?redirect_to=' + reverse('sale_create'))

    def test_create_form_existence(self):
        page = self.app.get(reverse('sale_create'), user='borodin_a_o')
        self.assertEqual(page.status_code, 200)
        self.assertEqual(len(page.forms), 1)

    def __login(self):
        self.client.login(username='borodin_a_o', password='password')

    def __another_login(self):
        seller = Seller.objects.create_user(email='another@sc.vsu.ru', username='another', password='password')
        self.client.login(username='another', password='password')
        return seller