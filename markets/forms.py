# forms.py
from django import forms
from .models import InventoryItem, Pack, SupplierInfo, Measurement, RestockHistory, Category


class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'barcode', 'barcode_type',
                  'quantity', 'price', 'discount', 'restock_level', "category", 'pack', 'supplier_info', 'expiration_date']


class PackForm(forms.ModelForm):
    class Meta:
        model = Pack
        fields = ["measurement_type", "packs_per_box",
                  "pack_quantity", 'pack_discount', 'price_per_pack']


class SupplierInfoForm(forms.ModelForm):
    class Meta:
        model = SupplierInfo
        fields = ['name', 'country', 'address', 'apartment',
                  'city', 'phone_number', 'zip_code']


class MeasurementForm(forms.ModelForm):
    class Meta:
        model = Measurement
        fields = ['type']


class RestockHistoryForm(forms.ModelForm):
    class Meta:
        model = RestockHistory
        fields = ['type_added', 'quantity_added']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']
