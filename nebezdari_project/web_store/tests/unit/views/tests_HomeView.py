from unittest.mock import patch

from django.urls import reverse
from django_mock_queries.query import MockSet
from django_webtest import WebTest

from nebezdari_project.views import HomeView
from web_store.models import Seller, Sale, Category


class HomeViewTests(WebTest):

    def setUp(self):
        self.seller_qs = MockSet(model=Seller)
        self.category_qs = MockSet(model=Category)

        self.seller = self.seller_qs.create(
            pk=1,
            username='borodin_a_o',
            email='borodin_a_o@sc.vsu.ru',
            password='password',
            phone='+7-952-952-52-38'
        )

        self.category1 = self.category_qs.create(category_name='Category1')
        self.category2 = self.category_qs.create(category_name='Category2')

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
        sale_qs = MockSet(model=Sale)
        sale1 = sale_qs.create(
            pk=1,
            title='1-title',
            body='1-body',
            photo='',
            price=1000,
            category=self.category1,
            author=self.seller
        )
        with patch.object(HomeView, 'get_queryset', return_value=sale_qs):
            response = self.client.get(reverse('home'))
            self.assertContains(response, '1-title')
            self.assertContains(response, '1-body')
            self.assertContains(response, 'Category1')
            self.assertContains(response, 1000)
            self.assertContains(response, self.seller.get_full_name())

    def test_two_sales(self):
        sale_qs = MockSet(model=Sale)
        sale1 = sale_qs.create(pk=1, title='1-title', body='1-body', photo='', price=1000, category=self.category1, author=self.seller)
        sale2 = sale_qs.create(pk=2, title='2-title', body='2-body', photo='', price=2000, category=self.category2, author=self.seller)

        with patch.object(HomeView, 'get_queryset', return_value=sale_qs):
            response = self.client.get(reverse('home'))
            self.assertContains(response, '1-title')
            self.assertContains(response, '2-title')

    def test_unauthorized_links(self):
        response = self.client.get(reverse('home'))
        self.assertIn(reverse('register'), response.content.decode())
        self.assertIn(reverse('login'), response.content.decode())
        self.assertNotIn(reverse('logout'), response.content.decode())

    def test_authorized_links(self):
        user = Seller.objects.create_user(
            username='username',
            password='password',
            email='email@gmail.com',
            phone='+7-952-952-52-38'
        )
        self.client.force_login(user, backend=None)
        response = self.client.get(reverse('home'))
        self.assertIn(reverse('logout'), response.content.decode())
        self.assertNotIn(reverse('register'), response.content.decode())
        self.assertNotIn(reverse('login'), response.content.decode())

    def test_pagination_is_ten(self):
        sale_qs = MockSet(model=Sale)
        for i in range(15):
            sale_qs.create(pk=i, title='Title ' + str(i), body='Body ' + str(i), photo='', price=1000 * i, category=self.category1, author=self.seller)

        with patch.object(HomeView, 'get_queryset', return_value=sale_qs):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)
            self.assertTrue('is_paginated' in response.context)
            self.assertTrue(response.context['is_paginated'] == True)
            self.assertTrue(len(response.context['sale_list']) == 10)