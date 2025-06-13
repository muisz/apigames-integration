from django.db import models

from apps.order.enums import OrderStatus
from apps.payment.enums import PaymentMethod
from apps.product.models import Product
from apps.utils.models import BaseModel


class Order(BaseModel):
    name = models.CharField(max_length=100)
    product = models.ForeignKey(Product, on_delete=models.PROTECT, related_name='orders')
    quantity = models.PositiveIntegerField()
    amount = models.PositiveIntegerField()
    payment_method = models.PositiveSmallIntegerField(choices=PaymentMethod.CHOICES)
    status = models.PositiveSmallIntegerField(choices=OrderStatus.CHOICES)
    order_id = models.CharField(max_length=100, unique=True)
    transaction_id = models.CharField(max_length=50, null=True, blank=True, unique=True, db_index=True)
    settlement_date = models.DateTimeField(null=True, blank=True)
    
    virtual_account = models.CharField(max_length=100, null=True, blank=True)

    order_destination = models.CharField(max_length=100)
