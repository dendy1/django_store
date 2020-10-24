from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView, DeleteView

from web_store.models import Seller


class SellerDetail(DetailView):
    model = Seller

class SellerUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    def test_func(self):
        return self.request.user == self.get_object()

    model = Seller
    fields = ('first_name', 'last_name', 'middle_name', 'phone')

class SellerDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    def test_func(self):
        return self.request.user.is_superuser

    model = Seller
    success_url = reverse_lazy('home')