# filters.py
from django.contrib.auth.models import Group
import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User


class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'is_superuser': ['exact'],  # You can add more fields if needed
        }


# filters.py


class GroupFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(
        lookup_expr='icontains', label='Group Name')

    class Meta:
        model = Group
        fields = ['name']


class UserGroupFilter(django_filters.FilterSet):
    email = django_filters.CharFilter(
        lookup_expr='icontains', label='Email')

    username = django_filters.CharFilter(
        lookup_expr='icontains', label='Username')

    class Meta:
        model = User
        fields = ['email', "username"]
