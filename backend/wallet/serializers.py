from rest_framework import serializers
from .models import Wallet, Transaction

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for the Transaction model.
    Provides a read-only representation of a single transaction, showing all
    relevant details for an audit trail.
    """
    class Meta:
        model = Transaction
        fields = ('id', 'amount', 'transaction_type', 'description', 'created_at')
        read_only_fields = fields

class WalletSerializer(serializers.ModelSerializer):
    """
    Serializer for the Wallet model.
    Includes the wallet's current balance and nests a list of all associated
    transactions using the TransactionSerializer.
    """
    transactions = TransactionSerializer(many=True, read_only=True)

    class Meta:
        model = Wallet
        fields = ('id', 'user', 'balance', 'updated_at', 'transactions')
        read_only_fields = ('id', 'user', 'balance', 'updated_at', 'transactions')

class AdminCreditSerializer(serializers.Serializer):
    """
    Serializer for the admin-only credit/debit functionality.
    It validates the required fields: amount, transaction type, and description.
    This is used for administrative adjustments to a user's wallet.
    """
    amount = serializers.IntegerField()
    transaction_type = serializers.ChoiceField(choices=Transaction.TransactionType.choices)
    description = serializers.CharField(max_length=255)
