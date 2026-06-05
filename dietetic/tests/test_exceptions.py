from django.urls import path
from rest_framework.test import APITestCase
from rest_framework.views import APIView
from rest_framework import status

class TriggerErrorView(APIView):
    def get(self, request):
        raise ValueError("Triggered unhandled error")

# Configurar URLs temporales para la prueba
urlpatterns = [
    path('trigger-error/', TriggerErrorView.as_view()),
]

class ExceptionHandlerTest(APITestCase):
    def test_unhandled_exception_returns_json_500(self):
        from django.test import override_settings
        with override_settings(ROOT_URLCONF='dietetic.tests.test_exceptions'):
            response = self.client.get('/trigger-error/')
            self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
            self.assertIn('success', response.data)
            self.assertFalse(response.data['success'])
            self.assertEqual(response.data['status_code'], 500)
            self.assertEqual(response.data['detail'], 'Ha ocurrido un error interno en el servidor.')
            self.assertEqual(response.data['error'], 'Triggered unhandled error')
