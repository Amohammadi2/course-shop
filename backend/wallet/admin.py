from django.contrib import admin
from .models import Wallet, Transaction

@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Wallet model.
    Displays user, balance, and timestamps, with search and ordering
    capabilities for effective wallet management.
    """
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    search_fields = ('user__username',)
    ordering = ('-updated_at',)
    readonly_fields = ('balance', 'user', 'created_at', 'updated_at')

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Transaction model.
    Provides a detailed transaction log with search and filtering options
    to easily audit wallet activities.
    """
    list_display = ('wallet', 'amount', 'transaction_type', 'created_at')
    search_fields = ('wallet__user__username', 'description')
    list_filter = ('transaction_type', 'created_at')
    ordering = ('-created_at',)
    # Make fields read-only as transactions should be immutable
    readonly_fields = ('wallet', 'amount', 'transaction_type', 'description', 'created_at')

    def has_add_permission(self, request):
        # Transactions should be created by the system, not manually
        return False

    def has_delete_permission(self, request, obj=None):
        # Transactions should not be deleted to maintain audit trail
        return False
