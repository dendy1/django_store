from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller


class LoginViewTests(WebTest):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_authentication_form_existence(self):
        page = self.app.get(reverse('login'))
        self.assertEqual(len(page.forms), 1)

    def test_error_on_empty_form(self):
        page = self.app.get(reverse('login'))
        page = page.form.submit()
        self.assertContains(page, 'This field is required.')

    def test_redirect_on_form_success(self):
        self.__register()

        page = self.app.get(reverse('login'))
        page.form['username'] = 'borodin_a_o'
        page.form['password'] = 'password'
        page = page.form.submit()
        self.assertRedirects(page, '/')

    def test_login(self):
        self.__register()

        response = self.client.post(reverse('login'), {
            'username': 'borodin_a_o',
            'password': 'password'
        }, follow=True)
        self.assertTrue(response.context['user'].is_active)

    def test_error_message_on_invalid_data(self):
        self.__register()

        response = self.client.post(reverse('login'), {
            'username': 'borodin_a_o',
            'password': 'password'
        }, follow=True)

        self.assertContains(response, 'Invalid data')

    def __register(self):
        seller = Seller.objects.create_user(
            username='borodin_a_o',
            email='borodin_a_o@sc.vsu.ru',
            password='password'
        )
        return seller