from django.contrib.auth.hashers import check_password
from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller


class RegisterViewTest(WebTest):

    def setUp(self) -> None:
        self.seller_valid_data = {
            'email': 'borodin_a_o@sc.vsu.ru',
            'username': 'borodin_a_o',
            'password': 'password',
            'first_name': 'Andrei',
            'last_name': 'Borodin',
            'middle_name': 'Olegovich',
            'phone': '+79529525238'
        }

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/register.html')

    def test_register_form_existence(self):
        page = self.app.get(reverse('register'))
        self.assertEqual(len(page.forms), 1)

    def test_error_on_empty_form(self):
        page = self.app.get(reverse('register'))
        page = page.form.submit()
        self.assertContains(page, 'This field is required.')

    def test_redirect_on_form_success(self):
        page = self.app.get(reverse('register'))
        page.form['email'] = self.seller_valid_data['email']
        page.form['username'] = self.seller_valid_data['username']
        page.form['password'] = self.seller_valid_data['password']
        page.form['first_name'] = self.seller_valid_data['first_name']
        page.form['last_name'] = self.seller_valid_data['last_name']
        page.form['middle_name'] = self.seller_valid_data['middle_name']
        page.form['phone'] = self.seller_valid_data['phone']
        page = page.form.submit()
        self.assertRedirects(page, '/')

    def test_seller_registration_on_form_success(self):
        page = self.app.get(reverse('register'))
        page.form['email'] = self.seller_valid_data['email']
        page.form['username'] = self.seller_valid_data['username']
        page.form['password'] = self.seller_valid_data['password']
        page.form['first_name'] = self.seller_valid_data['first_name']
        page.form['last_name'] = self.seller_valid_data['last_name']
        page.form['middle_name'] = self.seller_valid_data['middle_name']
        page.form['phone'] = self.seller_valid_data['phone']
        page = page.form.submit()

        self.assertEqual(Seller.objects.count(), 1)

        created_seller = Seller.objects.get(username__iexact=self.seller_valid_data['username'])
        self.assertEqual(created_seller.email, self.seller_valid_data['email'])
        self.assertEqual(created_seller.username, self.seller_valid_data['username'])

        self.assertNotEqual(created_seller.password, self.seller_valid_data['password'])
        self.assertTrue(check_password(self.seller_valid_data['password'], created_seller.password))

        self.assertEqual(created_seller.first_name, self.seller_valid_data['first_name'])
        self.assertEqual(created_seller.last_name, self.seller_valid_data['last_name'])
        self.assertEqual(created_seller.middle_name, self.seller_valid_data['middle_name'])
        self.assertEqual(created_seller.phone, self.seller_valid_data['phone'])