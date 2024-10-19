# filters.py
import django_filters
from .models import InventoryItem, Category, SupplierInfo, Measurement, Pack, RestockHistory


class InventoryItemFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryItem
        fields = {
            'name': ['icontains'],  # Filter by name (case insensitive)
            'barcode': ['exact'],   # Filter by barcode
            # Greater than or equal to, less than or equal to
            'quantity': ['gte', 'lte'],
            'price': ['gte', 'lte'],  # Price filters
            'discount': ['exact'],   # Filter by discount
            'date_added': ['date__gte', 'date__lte'],  # Date range filtering
            'supplier_info': ['exact'],
            'user': ['exact'],       # Filter by user
        }


class CategoryFilter(django_filters.FilterSet):
    class Meta:
        model = Category
        fields = {
            # Filter by name (case insensitive)
            'category_name': ['icontains'],
        }


class SupplierFilter(django_filters.FilterSet):
    class Meta:
        model = SupplierInfo
        fields = {
            # Filter by name (case insensitive)
            'name': ['icontains'],
            'created_by': ['exact'],   # Filter by barcode
            'city': ['exact'],
        }


class MeasurementFilter(django_filters.FilterSet):
    class Meta:
        model = Measurement
        fields = {
            # Filter by name (case insensitive)
            'type': ['icontains'],
        }


class PackageFilter(django_filters.FilterSet):
    class Meta:
        model = Pack
        fields = {
            'inventory_item': ['exact'],
            'measurement_type': ['exact'],
            'packs_per_box': ['icontains'],
            'pack_quantity': ['icontains'],
            'pack_discount': ['icontains'],
            'price_per_pack': ['icontains'],
        }


class RestockingFilter(django_filters.FilterSet):
    class Meta:
        model = RestockHistory
        fields = {
            'type_added': ['exact'],
            'initial_value': ['icontains'],
            'uuid': ['icontains'],
            'restocked_by': ['exact'],
            'quantity_added': ['icontains'],
            'restock_date': ['exact'],
        }


class POSFilter(django_filters.FilterSet):
    class Meta:
        model = InventoryItem
        fields = {
            'name': ['icontains'],  # Filter by name (case insensitive)
        }
