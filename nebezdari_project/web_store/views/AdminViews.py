from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView

from web_store.models import Category, Sale, Seller

class AdministratorMixin(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

class AdminCategoryView(AdministratorMixin, ListView):
    model = Category
    template_name = 'admin/category_list.html'
    paginate_by = 15

class AdminSaleView(AdministratorMixin, ListView):
    model = Sale
    template_name = 'admin/sale_list.html'
    paginate_by = 15

class AdminSellerView(AdministratorMixin, ListView):
    model = Seller
    template_name = 'admin/seller_list.html'
    paginate_by = 15