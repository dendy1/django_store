from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class Seller(AbstractUser):
    email = models.EmailField(max_length=50, blank=False)
    phone = models.CharField(max_length=30, blank=False)
    middle_name = models.CharField(max_length=150, blank=True)

    def __str__(self):
        return self.get_full_name() + ' [' + self.username + ', ' + self.email + ', ' + self.phone  + ']'

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        return reverse('seller_detail', kwargs={'pk': self.pk})

    def get_sales_list(self):
        return Sale.objects.filter(author__email=self.email).all()

class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return self.category_name

class Sale(models.Model):
    title = models.CharField(max_length=30, blank=False)
    body = models.TextField(max_length=10000, blank=False)
    category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(Seller, on_delete=models.CASCADE)
    price = models.IntegerField()
    photo = models.ImageField(upload_to='sales/photos/')

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    edited_at = models.DateTimeField(auto_now=True, editable=False)

    def get_absolute_url(self):
        return reverse('sale_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('sale_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('sale_delete', kwargs={'pk': self.pk})