from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField
from colorfield.fields import ColorField
from django_tenants.models import TenantMixin, DomainMixin
from phonenumber_field.modelfields import PhoneNumberField


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='tenant_owner')
    country = CountryField(blank_label="(select country)")
    address = models.CharField(
        max_length=500, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(null=True, blank=True)

    is_active = models.BooleanField(default=False)
    paid_until = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(blank=True, null=True)
    color = ColorField(default='#FF0000')
    updated = models.DateTimeField('Updated', auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass


class UserProducts(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_labels = models.ManyToManyField('AppLabel', blank=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s Products"


class AppLabel(models.Model):
    label = models.CharField(max_length=255, unique=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.label
