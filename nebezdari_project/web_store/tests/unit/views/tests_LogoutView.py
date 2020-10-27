from django.urls import reverse
from django_webtest import WebTest

from web_store.models import Seller


class LogoutViewTests(WebTest):

    def test_logout_redirect_to_home(self):
        self.__register()

        response = self.client.post(reverse('login'), {
            'username': 'borodin_a_o',
            'password': 'password'
        }, follow=True)
        self.assertTrue(response.context['user'].is_active)

        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('home'))

    def __register(self):
        seller = Seller.objects.create_user(
            username='borodin_a_o',
            email='borodin_a_o@sc.vsu.ru',
            password='password',
            phone='+7-952-952-52-38'
        )
        return seller