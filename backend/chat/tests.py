from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from .models import ChatCategory, ChatTicket

class ChatTicketCreationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.admin = User.objects.create_superuser(username='admin', password='password', email='admin@example.com')
        self.category = ChatCategory.objects.create(name='Technical Support')
        self.category.admins.add(self.admin)

        # Authenticate and get JWT
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_chat_ticket(self):
        """
        Ensure a user can create a new chat ticket.
        """
        url = reverse('user-chat-ticket-list')
        data = {'category': self.category.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ChatTicket.objects.filter(user=self.user, category=self.category).exists())

        # Check if the ticket was assigned to the admin
        ticket = ChatTicket.objects.get(user=self.user)
        self.assertEqual(ticket.assigned_admin, self.admin)
