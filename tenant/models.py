from django.db import models
from django.contrib.auth.models import User
from django_tenants.models import TenantMixin, DomainMixin
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Client(TenantMixin):
    name = models.CharField(max_length=100)
    # logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    owner = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, related_name='tenant_owner')
    country = CountryField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(
        max_length=500, unique=True, blank=True, null=True)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    paid_until = models.DateField(blank=True, null=True)
    on_trial = models.BooleanField(blank=True, null=True)
    color = models.CharField(
        max_length=7, help_text="Enter color in HEX format, e.g., #ffffff", blank=True, null=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created and synced when it is saved
    auto_create_schema = True


class Domain(DomainMixin):
    pass


class ClientLogo(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to='company_logos/', blank=True, null=True)
    created_on = models.DateField(auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)

    def __str__(self):
        return f'{self.client.owner.username} Profile'

    class Meta:
        verbose_name = 'Client Logo'
        verbose_name_plural = 'Client Logo'
