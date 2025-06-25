from rest_framework.test import APITestCase
from django.urls import reverse

class VendorAPITest(APITestCase):
    def test_create_vendor(self):
        url = reverse('vendor-list')  
        data = {
            "name": "Test Vendor",
            "phone_number": "123456789",
            "password_hash": "hash",
            "location": "Test Location",
            "shop_name": "Shop",
            "till_number": 123
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 201)