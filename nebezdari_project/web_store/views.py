from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, DeleteView, UpdateView, CreateView, ListView

from web_store.models import Sale, Seller, Category


class SaleDetail(DetailView):
    model = Sale

class SaleCreate(LoginRequiredMixin, CreateView):
    def get_success_url(self):
        return self.object.author.get_absolute_url()

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    model = Sale
    fields = ['title', 'body', 'category', 'photo', 'price']
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

class SaleUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.author.get_absolute_url()

    model = Sale
    fields = ['title', 'body', 'category', 'photo', 'price']
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

class SaleDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user == self.get_object().author

    def get_success_url(self):
        return self.object.author.get_absolute_url()

    model = Sale
    login_url = reverse_lazy('login')
    redirect_field_name = 'redirect_to'

class SellerDetail(DetailView):
    model = Seller

class SellerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.object

    model = Seller
    fields = ('email', 'password', 'first_name', 'last_name', 'middle_name', 'phone')

class SellerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Seller

class CategoryDetail(ListView):
    model = Category

class CategoryCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category
    fields = ['category_name']
    success_url = reverse_lazy('category_create')

class CategoryUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category

class CategoryDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Category