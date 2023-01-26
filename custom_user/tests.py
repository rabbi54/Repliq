from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import CustomUser
from rest_framework.authtoken.models import Token

# Create your tests here.
class TestTokenAuthentication(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username="rbb@gmail.com", password="password", phone="01382882211", email="rbb@gmail.com")
        token = Token.objects.create(user=self.user)

    def test_tokenAuth(self):
        url = "/api-token-auth/"
        response = self.client.post(
            path=url, data={"username": "rbb@gmail.com", "password": "password",}
        )
        self.assertEqual(response.status_code, 200)
