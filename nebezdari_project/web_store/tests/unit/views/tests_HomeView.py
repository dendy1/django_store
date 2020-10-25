from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller, Sale, Category


class HomeViewTests(WebTest):

    def setUp(self):
        self.seller = Seller.objects.create(email='borodin_a_o@sc.vsu.ru', username='borodin_a_o', password='password')
        self.categories = [
            Category.objects.create(category_name='Category1'),
            Category.objects.create(category_name='Category2'),
            Category.objects.create(category_name='Category3'),
            Category.objects.create(category_name='Category4')
        ]


    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')

    def test_zero_sales(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'No sales yet')

    def test_one_sale(self):
        sale = Sale.objects.create(title='1-title', body='1-body', photo='sales/photos/devar_logo1_HSGxUzx.jpg', price=1000, category=self.categories[0], author=self.seller)

        response = self.client.get(reverse('home'))
        self.assertContains(response, '1-title')
        self.assertContains(response, '1-body')
        self.assertContains(response, 'Category1')
        self.assertContains(response, self.seller.get_full_name())

    def test_two_sales(self):
        sale1 = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=self.categories[0], author=self.seller)
        sale2 = Sale.objects.create(title='2-title', body='2-body', photo='', price=2000, category=self.categories[1], author=self.seller)

        response = self.client.get(reverse('home'))
        self.assertContains(response, '1-title')
        self.assertContains(response, '2-title')

    def test_unauthorized_links(self):
        response = self.client.get(reverse('home'))
        self.assertIn(reverse('register'), response.content.decode())
        self.assertIn(reverse('login'), response.content.decode())
        self.assertNotIn(reverse('logout'), response.content.decode())

    def test_authorized_links(self):
        self.__login()

        response = self.client.get(reverse('home'))
        self.assertIn(reverse('logout'), response.content.decode())
        self.assertNotIn(reverse('register'), response.content.decode())
        self.assertNotIn(reverse('login'), response.content.decode())

    def test_pagination_is_ten(self):
        for i in range(15):
            sale = Sale.objects.create(title='1-title', body='1-body', photo='', price=1000, category=self.categories[2], author=self.seller)

        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['sale_list']) == 10)

    def __login(self):
        Seller.objects.create_user(email='andrei@sc.vsu.ru', username='username', password='password')
        self.client.login(username='username', password='password')