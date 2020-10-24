from django.test import TestCase

from web_store.models import Category


class CategoryModelTests(TestCase):

    def setUp(self) -> None:
        self.category = Category.objects.create(category_name='category')

    def test_category_string_representation(self):
        self.assertEqual(str(self.category), 'category')
