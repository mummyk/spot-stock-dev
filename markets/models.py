import string
import random
import uuid
from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
from django_countries.fields import CountryField


def generate_random_sku():
    """Generate a random 8-character SKU."""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))


class Measurement(models.Model):
    """Model to define different measurement systems."""
    MEASUREMENT_TYPES = [
        ('kg', 'Kilograms'),
        ('lb', 'Pounds'),
        ('l', 'Liters'),
        ('gal', 'Gallons'),
        ('m3', 'Cubic Meters'),
        ('ft3', 'Cubic Feet'),
    ]

    type = models.CharField(
        max_length=10, choices=MEASUREMENT_TYPES, unique=True)

    def __str__(self):
        return self.type


class InventoryItem(models.Model):
    """Model for inventory items."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, verbose_name="Item Name")
    description = models.TextField(blank=True, verbose_name="Description")
    barcode = models.CharField(
        max_length=100, unique=True, verbose_name="Barcode")
    barcode_image = models.ImageField(
        upload_to='barcode_images/', blank=True, null=True)  # Field for barcode image
    sku = models.CharField(max_length=8, unique=True,
                           verbose_name="SKU")
    category = models.ManyToManyField("Category", verbose_name="Category")
    barcode_type = models.CharField(
        max_length=10, verbose_name="Barcode Type", default="EAN13")
    image = models.ImageField(
        upload_to='inventory_images/', blank=True, null=True)
    quantity = models.PositiveIntegerField(
        default=0, verbose_name="Quantity in Stock")
    restock_level = models.PositiveIntegerField(
        default=5, verbose_name="Restock Level")  # Threshold for restocking
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price")
    discount = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="Discount", default=0.00)

    supplier_info = models.ManyToManyField(
        "SupplierInfo", blank=True, verbose_name="Supplier Info")  # Supplier information
    expiration_date = models.DateField(
        # Expiration date if applicable
        null=True, blank=True, verbose_name="Expiration Date")

    # Linking to the Pack model with a unique related_name
    pack = models.OneToOneField('Pack', on_delete=models.SET_NULL,
                                null=True, blank=True, related_name='inventory_items')

    date_added = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.sku:  # Generate SKU only if not already provided
            self.sku = generate_random_sku()

        # Ensure uniqueness by checking the SKU
        while InventoryItem.objects.filter(sku=self.sku).exists():
            self.sku = generate_random_sku()

        super(InventoryItem, self).save(*args, **kwargs)

    @classmethod
    def get_all_inventory(cls):
        """Return all inventory items."""
        return cls.objects.all()

    @classmethod
    def get_inventory_by_user(cls, user):
        """Return inventory items for a specific user."""
        return cls.objects.filter(user=user)

    def adjust_quantity(self, amount):
        """Adjust the quantity of the inventory item."""
        if self.quantity + amount < 0:
            raise ValidationError(
                "Insufficient stock to complete this operation.")

        self.quantity += amount
        self.save()

    @classmethod
    def validate_barcode(cls, barcode):
        """Check if the barcode exists in the inventory."""
        return cls.objects.filter(barcode=barcode).exists()


class Pack(models.Model):
    """Model for packs associated with Inventory Items."""
    inventory_item = models.ForeignKey(
        InventoryItem, on_delete=models.CASCADE, related_name='packs')
    measurement_type = models.ForeignKey(Measurement, on_delete=models.CASCADE)

    # Pack details
    packs_per_box = models.PositiveIntegerField(
        default=1, verbose_name="Packs per Box")

    pack_quantity = models.PositiveIntegerField(
        default=1, verbose_name="Packs Quantity")

    pack_discount = models.DecimalField(
        max_digits=3, decimal_places=2, verbose_name="Discount", default=0.00)

    price_per_pack = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Price per Pack")

    def __str__(self):
        return f"{self.packs_per_box} packs of {self.inventory_item.name} ({self.measurement_type})"


class RestockHistory(models.Model):
    """Model to track restocking events."""
    RESTOCKTYPE = [
        ('inventory', 'Inventory'),
        ('pack', 'Package/ Pack/ Container e.t.c'),

    ]
    type_added = models.CharField(max_length=20, choices=RESTOCKTYPE)
    initial_value = models.IntegerField()
    uuid = models.CharField(max_length=200)
    restocked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity_added = models.PositiveIntegerField()
    restock_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Restocked {self.quantity_added} of type {self.type_added} by {self.restocked_by} on {self.restock_date}"


class Category(models.Model):
    """Model to store category information."""
    category_name = models.CharField(max_length=30)

    def __str__(self):
        return self.category_name


class SupplierInfo(models.Model):
    """Model to store supplier information."""
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    country = CountryField()
    address = models.CharField(max_length=500)
    apartment = models.CharField(max_length=60)
    city = models.CharField(max_length=50)
    phone_number = PhoneNumberField(null=True, blank=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    created = models.DateTimeField('Created', auto_now_add=True)

    def __str__(self):
        return self.name


class SalesRecord(models.Model):
    """Model to track sales records."""

    SALE_STATUS = [
        ('completed', 'Completed'),
        ('pending', 'Pending'),
        ('refunded', 'Refunded'),
    ]

    PAYMENT_METHODS = [
        ('credit_card', 'Credit Card'),
        ('cash', 'Cash'),
        ('paypal', 'PayPal'),
        ('bank_transfer', 'Bank Transfer'),
        ('wallet', 'Wallet'),
    ]

    # Fields for the sales record
    # Unique sale identifier
    sale_id = models.CharField(
        max_length=8, verbose_name="SKU", editable=False, unique=True)
    # Reference to the sold inventory item
    item_id = models.CharField(
        max_length=200, blank=True, null=True, editable=False)
    quantity_sold = models.PositiveIntegerField(
        editable=False)  # Quantity of the item sold
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, editable=False)  # Total price of the sale
    # User who handled the sale
    sold_by = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    buyer_name = models.CharField(
        max_length=255, editable=False)  # Name of the buyer
    sale_date = models.DateTimeField(
        default=timezone.now, editable=False)  # Date and time of the sale
    status = models.CharField(
        max_length=10, choices=SALE_STATUS, default='completed')  # Status of the sale
    payment_method = models.CharField(
        # Payment method
        max_length=20, choices=PAYMENT_METHODS, default='cash', editable=False)

    def __str__(self):
        return f"Sale {self.sale_id} - {self.item_id} - {self.quantity_sold} units"

    class Meta:
        ordering = ['-sale_date']  # Orders by the most recent sale first

    def save(self, *args, **kwargs):
        if not self.sale_id:  # Generate sale_id only if not already provided
            self.sale_id = generate_random_sku()

        # Ensure uniqueness by checking the sale_id
        while InventoryItem.objects.filter(sale_id=self.sale_id).exists():
            self.sale_id = generate_random_sku()

        super(InventoryItem, self).save(*args, **kwargs)
