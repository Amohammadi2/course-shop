from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User

class UserAuthTests(APITestCase):
    def test_user_registration(self):
        """
        Ensure we can create a new user account.
        """
        url = reverse('user-registration')
        data = {'username': 'testuser', 'password': 'testpassword', 'email': 'test@example.com'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_login(self):
        """
        Ensure a registered user can log in and get a JWT.
        """
        # First, create a user
        User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')

        # Then, try to log in
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)
