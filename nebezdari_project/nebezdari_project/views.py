from django.views.generic import FormView, ListView

from web_store.forms import RegisterForm
from web_store.models import Seller, Sale


class HomeView(ListView):
    template_name = 'index.html'
    model = Sale
    paginate_by = 10

class RegisterView(FormView):
    form_class = RegisterForm
    model = Seller
    template_name = 'registration/register.html'
    success_url = '/'

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