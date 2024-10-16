# filters.py
from django.contrib.auth.models import User
import django_filters
from .models import Transaction, Payment, Wallet


class TransactionFilter(django_filters.FilterSet):
    class Meta:
        model = Transaction
        fields = {
            'transaction_type': ['exact'],
            # Greater than or equal to, less than or equal to
            'amount': ['gte', 'lte'],
            'timestamp': ['date__gte', 'date__lte'],  # Date range filtering
        }


class PaymentFilter(django_filters.FilterSet):
    class Meta:
        model = Payment
        fields = {
            'payment_method': ['exact'],
            'status': ['exact'],
            'timestamp': ['date__gte', 'date__lte'],  # Date range filtering
        }


# filters.py


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(
        field_name='username', lookup_expr='icontains', label='Username')
    email = django_filters.CharFilter(
        field_name='email', lookup_expr='icontains', label='Email')
    first_name = django_filters.CharFilter(
        field_name='first_name', lookup_expr='icontains', label='First Name')
    last_name = django_filters.CharFilter(
        field_name='last_name', lookup_expr='icontains', label='Last Name')

    # Adding a filter for wallet balance (optional)
    wallet_balance = django_filters.NumberFilter(
        field_name='wallet__balance', lookup_expr='exact', label='Wallet Balance')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'wallet_balance']

    def __init__(self, *args, **kwargs):
        # Get the current user from kwargs
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

        print(self.request)

        # Exclude the current user from the queryset
        if self.request and self.request.user.is_authenticated:
            self.queryset = self.queryset.exclude(id=self.request.user.id)

        # Prefetch wallets to avoid N+1 query problem
        self.queryset = self.queryset.prefetch_related('wallet')
