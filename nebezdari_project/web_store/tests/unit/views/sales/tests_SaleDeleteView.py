from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller, Category, Sale


class SaleDeleteViewTests(WebTest):

    def setUp(self):
        self.seller = Seller.objects.create_user(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password', phone='+7-952-952-52-38')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category = self.categories[0], author=self.seller)

    def test_delete_unauthorized_view(self):
        response = self.client.get(self.sale.get_delete_url())
        self.assertRedirects(response, reverse('login') + '?redirect_to=' + self.sale.get_delete_url())

    def test_delete_authorized_another_view(self):
        self.__another_login()

        response = self.client.get(self.sale.get_delete_url())
        self.assertEqual(response.status_code, 403)

    def test_delete_authorized_author_view(self):
        self.__login()

        response = self.client.get(self.sale.get_delete_url())
        self.assertEqual(response.status_code, 200)

    def test_delete_form_existence(self):
        page = self.app.get(self.sale.get_delete_url(), user='borodin_a_o')
        self.assertEqual(len(page.forms), 1)

    def test_redirect_on_form_success(self):
        page = self.app.get(self.sale.get_delete_url(), user='borodin_a_o')
        page = page.form.submit()
        self.assertRedirects(page, self.seller.get_absolute_url())

    def __login(self):
        self.client.login(username='borodin_a_o', password='password')

    def __another_login(self):
        Seller.objects.create_user(email='another@sc.vsu.ru', username='another', password='password')
        self.client.login(username='another', password='password')