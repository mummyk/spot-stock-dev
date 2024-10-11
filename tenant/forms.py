# forms.py
from django import forms
from .models import Client, ClientLogo
from phonenumber_field.formfields import PhoneNumberField
from django_countries.fields import CountryField


class ClientForm(forms.ModelForm):
    schema_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Your Sub domain'
    }))

    name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Company name'
    }))

   #  paid_until = forms.CharField(widget=forms.TextInput(attrs={
   #      'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
   #      'placeholder': 'Paid Until'
   #  }))

    color = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'Enter Your Color'
    }))
    country = CountryField(blank_label='(select country)').formfield(
        widget=forms.Select(attrs={
            'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
            'placeholder': 'United States'
        })
    )
    city = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. San Francisco'
    }))
    address = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. California'
    }))

    phone_number = PhoneNumberField(widget=forms.TextInput(attrs={
        'class': 'shadow-sm bg-gray-50 border border-gray-300 text-gray-900 sm:text-sm rounded-lg focus:ring-primary-500 focus:border-primary-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-primary-500 dark:focus:border-primary-500',
        'placeholder': 'e.g. +(12)3456 789'
    }))

   #  is_active = forms.BooleanField(
   #      required=False,  # Set to True if you want it to be mandatory
   #      widget=forms.CheckboxInput(attrs={
   #          "class": "w-4 h-4 border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:focus:ring-primary-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600",
   #      }),
   #      label='Is Active'  # Custom label
   #  )

   #  on_trial = forms.BooleanField(
   #      required=False,  # Set to True if you want it to be mandatory
   #      widget=forms.CheckboxInput(attrs={
   #          "class": "w-4 h-4 border-gray-300 rounded bg-gray-50 focus:ring-3 focus:ring-primary-300 dark:focus:ring-primary-600 dark:ring-offset-gray-800 dark:bg-gray-700 dark:border-gray-600",
   #      }),
   #      label='On Trial'  # Custom label
   #  )

    class Meta:
        model = Client
        fields = [
            'schema_name',
            'name',
            'city',
            'country',
            'address',
            'phone_number',
            'color'
        ]


class ClientLogoForm (forms.ModelForm):
    class Meta:
        model = ClientLogo
        fields = [
            "logo",  # This is the field that will be rendered as a file input

        ]
