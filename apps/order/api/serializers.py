from rest_framework import serializers

from apps.order.enums import OrderStatus
from apps.order.models import Order
from apps.payment.enums import PaymentMethod
from apps.utils.serializers import EnumChoiceField


class CreateOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('product', 'quantity', 'payment_method', 'order_destination')

class DetailOrderSerializer(serializers.ModelSerializer):
    payment_method = EnumChoiceField(PaymentMethod)
    status = EnumChoiceField(OrderStatus)

    class Meta:
        model = Order
        fields = (
            'order_id',
            'name',
            'payment_method',
            'amount',
            'status',
            'virtual_account',
        )
