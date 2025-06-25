from django.test import TestCase
from users.models import Vendor, Buyer
from order.models import Order
from payments.models import Payment

class PaymentModelTest(TestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Test Vendor",
            phone_number="1234567890",
            password_hash="hashedpassword",
            location="Test City",
            shop_name="Test Shop",
            till_number=123456,  # must be unique
        )
        self.buyer = Buyer.objects.create(
            name="Test Buyer",
            password_hash="buyerhashedpassword",
            location="Buyer City",
            phone_number="0987654321",
        )
        self.order = Order.objects.create(
            vendor=self.vendor,
            buyer=self.buyer,
            total_price=100.50,
            status="Pending"
        )

    def test_create_payment(self):
        payment = Payment.objects.create(
            order=self.order,
            method="Credit Card",
            status="Completed",
            amount=99.99,
        )
        self.assertEqual(payment.order, self.order)
        self.assertEqual(payment.method, "Credit Card")
        self.assertEqual(payment.status, "Completed")
        self.assertEqual(float(payment.amount), 99.99)
        self.assertIsNotNone(payment.created_at)

    def test_payment_str(self):
        payment = Payment.objects.create(
            order=self.order,
            method="Paypal",
            status="Pending",
            amount=50,
        )
        expected_str = f"Payment {payment.payment_id} for Order {self.order.order_id} ({payment.status})"
        self.assertEqual(str(payment), expected_str)

    def test_related_name_payments(self):
        payment1 = Payment.objects.create(
            order=self.order,
            method="Bank Transfer",
            status="Completed",
            amount=150.50,
        )
        payment2 = Payment.objects.create(
            order=self.order,
            method="Paypal",
            status="Pending",
            amount=80.00,
        )
        self.assertIn(payment1, self.order.payments.all())
        self.assertIn(payment2, self.order.payments.all())