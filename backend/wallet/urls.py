from django.urls import path
from .views import UserWalletView, AdminWalletCreditView

urlpatterns = [
    path('', UserWalletView.as_view(), name='user-wallet'),
    path('admin/credit/<int:user_id>/', AdminWalletCreditView.as_view(), name='admin-wallet-credit'),
]
