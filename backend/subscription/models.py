from django.db import models
from django.core.exceptions import ValidationError
from users.models import User
from product.models import Product

FREQUENCY_CHOICES = [
    ('weekly', 'Weekly'),
    ('monthly', 'Monthly'),
    ('Twice a week', 'Twice a week'),
]

UNIT_CHOICES = [
    ('kg', 'Kg'),
    ('bunch', 'Bunch'),
]

class SubscriptionBox(models.Model):
    schedule_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='customer_subscriptions',
        limit_choices_to={'type': 'customer'},
        help_text="User of type 'customer'",
        blank=True,
        null=True
    )
    vendor = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='vendor_subscriptions',
        limit_choices_to={'type': 'vendor'},
        help_text="User of type 'vendor'",
        blank=True,
        null=True
    )



    name = models.CharField(max_length=100)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES)
    price = models.PositiveIntegerField()
    start_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=100)

    def __str__(self):
        return f"Subscription {self.name} for {self.buyer.name}"

    def clean(self):
        super().clean()
        if self.buyer and self.buyer.type != 'customer':
            raise ValidationError({"buyer": "Buyer must be of type 'customer'."})
        if self.vendor and self.vendor.type != 'vendor':
            raise ValidationError({"vendor": "Vendor must be of type 'vendor'."})

    class Meta:
        verbose_name = "Subscription Box"
        verbose_name_plural = "Subscription Boxes"

class ScheduledItem(models.Model):
    scheduled_item_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    schedule = models.ForeignKey(
        SubscriptionBox,
        on_delete=models.CASCADE,
        related_name='scheduled_items'
    )
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2 )
    quantity = models.IntegerField()
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES)

    def __str__(self):
        return f"{self.quantity}{self.unit} {self.product.name} (Schedule {self.schedule.schedule_id})"

    class Meta:
        verbose_name = "Scheduled Item"
        verbose_name_plural = "Scheduled Items"