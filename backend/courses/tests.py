from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import User
from wallet.models import Wallet
from .models import Course, Enrollment

class CourseEnrollmentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.course = Course.objects.create(title='Test Course', price=10)

        # Give the user some credits
        self.user.wallet.balance = 20
        self.user.wallet.save()

        # Authenticate and get JWT
        url = reverse('token_obtain_pair')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_enroll_in_course(self):
        """
        Ensure a user can enroll in a course if they have enough credits.
        """
        url = reverse('enroll-course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Enrollment.objects.filter(user=self.user, course=self.course).exists())

        # Check if credits were deducted
        self.user.wallet.refresh_from_db()
        self.assertEqual(self.user.wallet.balance, 10)

    def test_enroll_insufficient_credits(self):
        """
        Ensure a user cannot enroll in a course if they have insufficient credits.
        """
        # Set user's balance to be less than the course price
        self.user.wallet.balance = 5
        self.user.wallet.save()

        url = reverse('enroll-course', kwargs={'course_id': self.course.id})
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Enrollment.objects.filter(user=self.user, course=self.course).exists())
