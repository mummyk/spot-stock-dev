from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Client, Domain


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
