from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, ListView
from django_filters.views import FilterView

from web_store.filters import SaleFilter
from web_store.forms import RegisterForm
from web_store.models import Seller, Sale


class HomeView(FilterView):
    template_name = 'index.html'
    filterset_class = SaleFilter
    queryset = Sale.objects.order_by('-created_at')
    paginate_by = 10

class RegisterView(FormView):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().get(request, args, kwargs)

    def form_valid(self, form):
        seller = Seller.objects.create_user(
            form.cleaned_data['username'],
            form.cleaned_data['email'],
            form.cleaned_data['password'],
        )
        seller.phone = form.cleaned_data['phone']
        seller.first_name = form.cleaned_data['first_name']
        seller.last_name = form.cleaned_data['last_name']
        seller.middle_name = form.cleaned_data['middle_name']
        seller.save()
        return super().form_valid(form)

    form_class = RegisterForm
    model = Seller
    template_name = 'registration/register.html'
    success_url = reverse_lazy('home')

class AuthenticationView(LoginView):

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(self.request.user)

        return super().get(request, args, kwargs)

    success_url = reverse_lazy('home')