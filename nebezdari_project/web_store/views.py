from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView

from web_store.models import Sale, Seller, Category


class SaleDetail(DetailView):
    model = Sale

class SaleCreate(LoginRequiredMixin, CreateView):
    def get_success_url(self):
        return self.get_object().author.get_absolute_url()

    model = Sale
    fields = ['title', 'body', 'categories', 'photo', 'price']
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class SaleUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.get_object().author.get_absolute_url()

    model = Sale
    fields = ['title', 'body', 'categories', 'photo', 'price']
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class SaleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.get_object().author.get_absolute_url()

    model = Sale
    login_url = '/login/'
    redirect_field_name = 'redirect_to'

class SellerDetail(DetailView):
    model = Seller

class SellerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object()

    model = Seller

class SellerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_staff

    model = Seller

class CategoryDetail(DetailView):
    model = Category

class CategoryUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_staff

    model = Category

class CategoryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_staff

    model = Category