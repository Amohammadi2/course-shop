from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Wallet(models.Model):
    """
    Represents a user's internal credit wallet.
    Each user has a one-to-one relationship with a wallet, which holds their
    credit balance. The balance is a positive integer and defaults to zero.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='wallet')
    balance = models.PositiveIntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

class Transaction(models.Model):
    """
    Represents a single transaction within a wallet.
    This model provides a complete audit trail of all credit changes.
    Transactions can be of various types (e.g., deposit, purchase) and
    record the amount, the resulting balance, and a timestamp.
    """
    class TransactionType(models.TextChoices):
        DEPOSIT = 'DEPOSIT', 'Deposit'
        PURCHASE = 'PURCHASE', 'Purchase'
        REFUND = 'REFUND', 'Refund'
        ADMIN_ADJUSTMENT = 'ADMIN_ADJUSTMENT', 'Admin Adjustment'

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField()  # Can be positive or negative
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    description = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} of {self.amount} for {self.wallet.user.username}"
