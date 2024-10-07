from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


class Profile(models.Model):
    """User profile fields"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/', blank=True, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    country = CountryField()
    city = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    gender = models.CharField(max_length=10)
    phone_number = PhoneNumberField(null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created = models.DateTimeField('Created', auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} Profile'

    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
