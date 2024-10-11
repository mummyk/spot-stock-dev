from .models import Client
from django_filters import rest_framework as filters


class ClientFilter(filters.FilterSet):
    class Meta:
        model = Client
        fields = {
            'name': ['exact', 'icontains'],
            'owner': ['exact'],
            'is_active': ['exact'],
        }
