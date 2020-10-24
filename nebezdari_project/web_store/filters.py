import django_filters

from web_store.models import Sale


class SaleFilter(django_filters.FilterSet):
    class Meta:
        model = Sale
        fields = ['category']