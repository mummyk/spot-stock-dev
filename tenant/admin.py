from django.contrib import admin

# Register your models here.
from django_tenants.admin import TenantAdminMixin

from .models import Client, Domain, UserProducts, AppLabel


class DomainInline(admin.TabularInline):
    model = Domain
    max_num = 1


@admin.register(Client)
class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = (
        "schema_name",
        "owner",
        "is_active",
        "created_on",
        "country",
    )
    inlines = [DomainInline]


@admin.register(UserProducts)
class UserProductAdmin(admin.ModelAdmin):
    list_display = ('user',)


admin.site.register(AppLabel)
