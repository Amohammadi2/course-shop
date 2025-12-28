from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import Wallet

class WalletTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Authenticate and get JWT
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_wallet_creation(self):
        """
        Ensure a wallet is automatically created for a new user.
        """
        self.assertTrue(hasattr(self.user, 'wallet'))
        self.assertEqual(self.user.wallet.balance, 0)

    def test_get_wallet_details(self):
        """
        Ensure an authenticated user can retrieve their own wallet details.
        """
        url = reverse('user-wallet')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['balance'], 0)
