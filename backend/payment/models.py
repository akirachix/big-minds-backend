from django.db import models
from users.models import User
from product.models import Product
from orders.models import Order

class Payment(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
    )

    payment_id = models.AutoField(primary_key=True)
    order= models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='payments',
        help_text="Associated order"
    )
    method = models.CharField(
        max_length=100,
        default='M-Pesa',
        help_text="Payment method"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Payment status"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Payment amount"
    )
    merchant_request_id = models.CharField(max_length=100, unique=True)
    checkout_request_id = models.CharField(
        max_length=100,
        unique=True,
        blank=True,
        null=True,
        help_text="Unique Checkout Request ID from M-Pesa"
    )
    result_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
        help_text="M-Pesa Result Code"
    )
    result_desc = models.TextField(
        blank=True,
        null=True,
        help_text="M-Pesa Result Description"
    )
    mpesa_receipt_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
        help_text="M-Pesa Transaction Receipt Number"
    )
    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Phone number used for payment"
    )
    transaction_date = models.DateTimeField(
        blank=True,
        null=True,
        help_text="Date and time of the transaction"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the payment record was created"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the payment record was last updated"
    )

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        indexes = [
            models.Index(fields=['merchant_request_id']),
            models.Index(fields=['checkout_request_id']),
            models.Index(fields=['status']),
            models.Index(fields=['order_id']),  
        ]

    def __str__(self):
        return f"Payment {self.payment_id} for Order {self.order_id.order_id} ({self.status})"