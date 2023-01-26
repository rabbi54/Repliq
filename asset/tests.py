from django.test import TestCase
from .models import *
import json
from asset.models import *
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

class Factory():
    def create_instances(self):
        user = CustomUser.objects.create_user(username="rbb@gmail.com", password="password", phone="01382882211", email="rbb@gmail.com")
        user2 = CustomUser.objects.create_user(username="rbb2@gmail.com", password="password", phone="01382881211", email="rbb2@gmail.com")
        company = Company.objects.create(name='BD', address='Banani, Dhaka', contact_no='01786476455')
        employee_admin = Employee.objects.create(user=user, employee_id=17, company=company, is_company_admin=True, in_service=True)
        employee = Employee.objects.create(user=user2, employee_id=12, company=company, is_company_admin=False, in_service=True)
        brand = Brand.objects.create(name='Laptop')
        asset = Asset.objects.create(company=company,  brand=brand, is_available=True)
        asset = Asset.objects.create(company=company, brand=brand, is_available=False)
        asset = Asset.objects.create(company=company, brand=brand, is_available=False)

        return (user, user2, company, employee, employee_admin, asset)

class AssetTest(TestCase):
    def setUp(self):
        factory = Factory()
        (self.user1, self.user2, self.compnay, self.employee, self.employee_admin, self.asset) = factory.create_instances()
        self.token_user1 = Token.objects.create(user=self.user1)
        self.token_user2 = Token.objects.create(user=self.user2)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='token ' + self.token_user1.key)

    def test_asset_in_stock(self):
        target_url = "/api/asset_in_stock/"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 200)
        
        response = response.json()
        self.assertEqual(len(response), 1)

    def test_asset_not_in_stock(self):
        target_url = "/api/asset_not_in_stock/"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 200)
        
        response = response.json()
        self.assertEqual(len(response), 2)

    def test_asset_in_stock_unauthorized(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token_user2.key)
        target_url = "/asset/api/asset_in_stock/"
        response = self.client.get(path=target_url)
        self.assertEqual(response.status_code, 404)
        