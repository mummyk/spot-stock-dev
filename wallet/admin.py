from django.contrib import admin

# Register your models here.
from .models import Wallet, Transaction, Payment

admin.site.register(Wallet)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "wallet",
        "transaction_type",
        "amount",
        "timestamp",
    )
    list_filter = ("wallet",)  # Group by wallet


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = (
        "transaction",
        "payment_method",
        "status",
        "payment_reference",
        "processed_at",
    )
    list_filter = ("transaction",)  # Group by transaction
