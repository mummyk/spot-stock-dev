# forms.py
from django import forms


class UserSearchForm(forms.Form):
    query = forms.CharField(label='Search Users', max_length=100)
