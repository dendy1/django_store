from django_webtest import WebTest

from web_store.models import Seller, Category, Sale


class SaleDetailViewTest(WebTest):

    def setUp(self):
        self.seller = Seller.objects.create(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password', phone='+7-952-952-52-38')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2')
        ]
        self.sale = Sale.objects.create(title='1-title', body='1-body', photo='', category = self.categories[0], price=1000, author=self.seller)

    def test_detail_view(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_title_in_sale(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertContains(response, self.sale.title)

    def test_body_in_sale(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertContains(response, self.sale.body)

    def test_categories_in_sale(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertContains(response, self.sale.category)

    def test_price_in_sale(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertContains(response, self.sale.price)

    def test_author_information_in_sale(self):
        response = self.client.get(self.sale.get_absolute_url())
        self.assertContains(response, self.sale.author.get_full_name())
        self.assertContains(response, self.sale.author.email)
        self.assertContains(response, self.sale.author.phone)