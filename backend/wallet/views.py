from django.db import transaction
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from .models import Wallet, Transaction
from .serializers import WalletSerializer, AdminCreditSerializer
from users.models import User

@extend_schema(
    summary="Retrieve the current user's wallet",
    description="Fetches the wallet details for the currently authenticated user, including their balance and a full transaction history."
)
class UserWalletView(generics.RetrieveAPIView):
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.wallet

@extend_schema(
    summary="Admin: Credit or debit a user's wallet",
    description="Allows an admin to manually adjust a user's wallet balance. A transaction record is created for each adjustment. Restricted to admin users."
)
class AdminWalletCreditView(APIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = AdminCreditSerializer

    def post(self, request, user_id):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(id=user_id)
                wallet = user.wallet
            except (User.DoesNotExist, Wallet.DoesNotExist):
                return Response({"error": "User or wallet not found."}, status=status.HTTP_404_NOT_FOUND)

            amount = serializer.validated_data['amount']
            transaction_type = serializer.validated_data['transaction_type']
            description = serializer.validated_data['description']

            try:
                with transaction.atomic():
                    wallet.balance += amount
                    wallet.save()

                    Transaction.objects.create(
                        wallet=wallet,
                        amount=amount,
                        transaction_type=transaction_type,
                        description=description
                    )

                return Response(WalletSerializer(wallet).data, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
