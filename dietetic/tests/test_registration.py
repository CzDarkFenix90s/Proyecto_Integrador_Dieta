from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from dietetic.models import Paciente

class RegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register') # Assuming 'register' is the name of the URL

    def test_user_registration_creates_paciente_profile(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
            "password2": "password123"
        }

        response = self.client.post(self.register_url, data, format='json')

        # Check if registration was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if user was created
        user = User.objects.get(username="testuser")
        self.assertIsNotNone(user)

        # Check if Paciente profile was created automatically
        paciente = Paciente.objects.filter(user=user).first()
        self.assertIsNotNone(paciente, "Paciente profile should be created automatically upon registration")
        self.assertEqual(paciente.full_name, "testuser")
        self.assertEqual(paciente.status, "activo")
