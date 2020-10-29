from django.test import TestCase

from web_store.models import Category


class CategoryModelTests(TestCase):

    def test_category_string_representation(self):
        category = Category(category_name='Category1')
        self.assertEqual(str(category), 'Category1')
