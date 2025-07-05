from django.test import TestCase
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from django.utils import timezone
from payment.models import Payment
from orders.models import Order
from users.models import User
from product.models import Product

class PaymentModelTests(TestCase):
    def setUp(self):
        self.customer = User.objects.create(
            type='customer',
            name='Test Customer'
        )
        self.vendor = User.objects.create(
            type='vendor',
            name='Test Vendor'
        )
    
        self.product = Product.objects.create(
            name='Test Product'
        )
   
        self.order = Order.objects.create(
            buyer=self.customer,
            vendor=self.vendor
        )
       
        self.payment = Payment.objects.create(
            order=self.order,
            method='M-Pesa',
            status='pending',
            amount=100.00,
            merchant_request_id='MERCHANT123',
            checkout_request_id='CHECKOUT123',
            result_code='0',
            result_desc='Success',
            mpesa_receipt_number='RECEIPT123',
            phone_number='+254712345678',
            transaction_date=timezone.now()
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.order, self.order)
        self.assertEqual(self.payment.method, 'M-Pesa')
        self.assertEqual(self.payment.status, 'pending')
        self.assertEqual(self.payment.amount, 100.00)
        self.assertEqual(self.payment.merchant_request_id, 'MERCHANT123')
        self.assertEqual(self.payment.checkout_request_id, 'CHECKOUT123')
        self.assertEqual(self.payment.result_code, '0')
        self.assertEqual(self.payment.result_desc, 'Success')
        self.assertEqual(self.payment.mpesa_receipt_number, 'RECEIPT123')
        self.assertEqual(self.payment.phone_number, '+254712345678')
        self.assertIsNotNone(self.payment.transaction_date)
    def test_unique_merchant_request_id(self):
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                order=self.order,
                method='M-Pesa',
                status='pending',
                amount=50.00,
                merchant_request_id='MERCHANT123'  
            )

    def test_unique_checkout_request_id(self):
        with self.assertRaises(IntegrityError):
            Payment.objects.create(
                order=self.order,
                method='M-Pesa',
                status='pending',
                amount=50.00,
                merchant_request_id='MERCHANT456',
                checkout_request_id='CHECKOUT123'  
            )

    def test_nullable_checkout_request_id(self):
        payment = Payment.objects.create(
            order=self.order,
            method='M-Pesa',
            status='pending',
            amount=50.00,
            merchant_request_id='MERCHANT456',
            checkout_request_id=None
        )
        self.assertIsNone(payment.checkout_request_id)

    def test_status_choices(self):
        payment = Payment.objects.create(
            order=self.order,
            method='M-Pesa',
            status='success',
            amount=50.00,
            merchant_request_id='MERCHANT789',
            transaction_date=timezone.now()
        )
        self.assertEqual(payment.status, 'success')

        with self.assertRaises(ValidationError):
            invalid_payment = Payment(
                order=self.order,
                method='M-Pesa',
                status='invalid',  
                amount=50.00,
                merchant_request_id='MERCHANT999'
            )
            invalid_payment.full_clean()

    def test_amount_decimal_places(self):
        payment = Payment.objects.create(
            order=self.order,
            method='M-Pesa',
            status='pending',
            amount=50.99,
            merchant_request_id='MERCHANT101',
            transaction_date=timezone.now()
        )
        self.assertEqual(payment.amount, 50.99)

    def test_default_values(self):
        payment = Payment.objects.create(
            order=self.order,
            amount=75.00,
            merchant_request_id='MERCHANT202',
            transaction_date=timezone.now()
        )
        self.assertEqual(payment.method, 'M-Pesa')
        self.assertEqual(payment.status, 'pending')

    def test_nullable_fields(self):
        payment = Payment.objects.create(
            order=self.order,
            method='M-Pesa',
            status='pending',
            amount=50.00,
            merchant_request_id='MERCHANT303',
            result_code=None,
            result_desc=None,
            mpesa_receipt_number=None,
            phone_number=None,
            transaction_date=None
        )
        self.assertIsNone(payment.result_code)
        self.assertIsNone(payment.result_desc)
        self.assertIsNone(payment.mpesa_receipt_number)
        self.assertIsNone(payment.phone_number)
        self.assertIsNone(payment.transaction_date)
