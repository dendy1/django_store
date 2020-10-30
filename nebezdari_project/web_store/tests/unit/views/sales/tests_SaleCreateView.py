from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller, Category, Sale


class SaleCreateViewTests(WebTest):

    def setUp(self):
        self.seller = Seller.objects.create_user(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password', phone='+7-952-952-52-38')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=self.categories[1], author=self.seller)

    def test_create_view(self):
        response = self.client.get(reverse('sale_create'))
        self.assertRedirects(response, reverse('login') + '?redirect_to=' + reverse('sale_create'))

    def test_create_form_existence(self):
        page = self.app.get(reverse('sale_create'), user='borodin_a_o')
        self.assertEqual(page.status_code, 200)
        self.assertEqual(len(page.forms), 1)