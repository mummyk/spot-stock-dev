from django.contrib import admin
from .models import Pack, Category, InventoryItem, Measurement, RestockHistory, SupplierInfo, SalesRecord
# Register your models here.


admin.site.register(Pack)
admin.site.register(Category)
admin.site.register(InventoryItem)
admin.site.register(Measurement)
admin.site.register(RestockHistory)
admin.site.register(SupplierInfo)
admin.site.register(SalesRecord)
