import uuid
from decimal import Decimal
from django.db import transaction
from django.db import models, transaction
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.hashers import make_password, check_password


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    balance = models.DecimalField(
        max_digits=12, decimal_places=2, default=Decimal('0.00'))
    password = models.CharField(
        max_length=128, null=True, blank=True)  # Hashed password field
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user.username}'s wallet - Balance: {self.balance}"

    def clean(self):
        """Ensure balance is not negative"""
        if self.balance < 0:
            raise ValidationError("Wallet balance must be positive")

    def set_password(self, raw_password):
        """Set the wallet's password (hashed)"""
        self.password = make_password(raw_password)
        self.save()

    def check_password(self, raw_password):
        """Check the wallet's password"""
        return check_password(raw_password, self.password)

    def deposit(self, amount):
        try:
            """Increase the wallet balance by the amount with proper validation."""
            amount = Decimal(amount)  # Convert the amount to Decimal

            if amount <= 0:
                raise ValidationError("Deposit amount must be positive")

            # Maximum balance limit
            if self.balance + amount > Decimal('1000000000000.00'):
                raise ValidationError("Maximum Deposit limit reached")

            # Proceed with the deposit
            with transaction.atomic():
                self.balance += amount
                self.clean()  # Ensure no negative balance or other issues
                self.save()  # Save the updated balance to the database

            return self.balance
        except ValidationError as e:
            # Log the error
            print(f"Error during Deposit: {str(e)}")
            raise e

    def withdraw(self, amount, password):
        """Decrease the wallet balance by the amount with proper validation."""
        try:
            amount = Decimal(amount)  # Convert amount to Decimal

            if amount <= 0:
                raise ValidationError("Withdraw amount must be positive")

            # Maximum withdrawal limit check
            if amount > Decimal('10000.00'):  # Max per Withdraw
                raise ValidationError("Maximum withdrawal limit reached")

            if self.balance < amount:
                raise ValidationError("Insufficient balance to withdraw")

            # Check if the provided password is correct
            if not check_password(password, self.password):
                raise ValidationError("Incorrect password.")

            # Proceed with the withdrawal
            with transaction.atomic():
                self.balance -= amount
                self.clean()  # Ensure no negative balance or other issues
                self.save()  # Save the updated balance to the database

            return self.balance
        except ValidationError as e:
            # Log the error
            print(f"Error during withdrawal: {str(e)}")
            raise e


class Transaction(models.Model):
    TRANSACTION_TYPE = [('deposit', 'Deposit'), ('withdrawal',
                                                 'Withdrawal'), ('transfer', 'Transfer'),]

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    transaction_uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    transaction_type = models.CharField(
        max_length=15, choices=TRANSACTION_TYPE)
    to_user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.wallet.user.username}-{self.transaction_type} of {self.amount} on {self.timestamp}"


class Payment(models.Model):
    # Every payment is linked to a transaction
    transaction = models.OneToOneField(Transaction, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    payment_method = models.CharField(
        max_length=15)
    status = models.CharField(max_length=10, default='pending')
    # Reference for third-party payments (e.g., Stripe ID)
    payment_reference = models.CharField(
        max_length=255, null=True, blank=True)
    authorization_code = models.CharField(
        max_length=255, null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Payment {self.payment_reference} - {self.payment_method} - {self.status}"
