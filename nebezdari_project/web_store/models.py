from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator, MinLengthValidator, EmailValidator
from django.db import models
from django.urls import reverse

# Добавить валидацию
class Seller(AbstractUser):
    alphanumeric_symbols = RegexValidator(r'^[0-9a-zA-Z_@+.-]*$', 'Only alphanumeric characters are allowed.')
    alpha_only = RegexValidator(r'^[a-zA-Zа-яА-Я]*$', 'Only alphanumeric characters are allowed.')
    phone_validator = RegexValidator(r'^[0-9+-]*$')
    email_validator = RegexValidator(r'^[0-9a-zA-Z_@+.-]*$', 'Only english alphanumeric characters are allowed.')

    username = models.CharField(max_length=150, unique=True, blank=False, validators=[alphanumeric_symbols])
    password = models.CharField(max_length=150, blank=False, validators=[MinLengthValidator(8)])
    email = models.CharField(max_length=50, unique=True, blank=False, validators=[EmailValidator()])

    phone = models.CharField(max_length=30, validators=[phone_validator])

    first_name = models.CharField(max_length=150, blank=True, validators=[alpha_only])
    last_name = models.CharField(max_length=150, blank=True, validators=[alpha_only])
    middle_name = models.CharField(max_length=150, blank=True, validators=[alpha_only])

    def save(self, *args, **kwargs):
        #self.clean_fields()  # validate individual fields
        #self.clean()  # validate constraints between fields
        #self.validate_unique()  # validate uniqness of fields
        return super(AbstractUser, self).save(*args, **kwargs)

    def __str__(self):
        return self.get_full_name() + ' [' + self.username + ', ' + self.email + ', ' + self.phone  + ']'

    def get_full_name(self):
        return self.last_name + ' ' + self.first_name + ' ' + self.middle_name

    def get_absolute_url(self):
        return reverse('seller_detail', kwargs={'pk': self.pk})

    def get_update_url(self):
        return reverse('seller_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('seller_delete', kwargs={'pk': self.pk})

    def get_sales_list(self):
        return Sale.objects.filter(author__email=self.email).all()

class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=False)

    def get_absolute_url(self):
        return reverse('home') + '?category=' + str(self.pk)

    def get_update_url(self):
        return reverse('category_update', kwargs={'pk': self.pk})

    def get_delete_url(self):
        return reverse('category_delete', kwargs={'pk': self.pk})

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

    def __str__(self):
        return 'Sale ' + self.title + ' in ' + str(self.category)