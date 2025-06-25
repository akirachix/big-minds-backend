from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from order.models import Order
from api.models import Payment
from users.models import Vendor
from users.models import Buyer
class OrderPaymentAPITestCase(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(name="Test Vendor", till_number= "34567899")
        self.buyer = Buyer.objects.create(name="Test Buyer")
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=1000.00,
            status="pending"
        )
    def test_create_order(self):
        url = reverse('order-list')
        data = {
            "vendor": self.vendor.pk,
            "buyer": self.buyer.pk,
            "total_price": "500.00",
            "status": "approved"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(response.data['total_price'], "500.00")
    def test_list_orders(self):
        url = reverse('order-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data or isinstance(response.data, list))
    def test_create_payment(self):
        url = reverse('payment-list')
        data = {
            "order_id": self.order.pk,
            "method": "credit_card",
            "status": "pending",
            "amount": "1000.00"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(response.data['amount'], "1000.00")
    def test_list_payments(self):
        Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('results' in response.data or isinstance(response.data, list))
    def test_retrieve_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['amount'], "500.00")
    def test_update_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        data = {
            "order_id": self.order.pk,
            "method": "credit_card",
            "status": "pending",
            "amount": "750.00"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        payment.refresh_from_db()
        self.assertEqual(payment.amount, 750.00)
    def test_delete_payment(self):
        payment = Payment.objects.create(order=self.order, method="cash", status="completed", amount=500.00)
        url = reverse('payment-detail', args=[payment.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Payment.objects.filter(pk=payment.pk).exists())
