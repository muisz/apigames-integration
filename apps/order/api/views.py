import uuid
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError, NotFound

from apps.order.api.serializers import CreateOrderSerializer, DetailOrderSerializer
from apps.order.enums import OrderStatus
from apps.order.models import Order
from apps.libs.payments import payment_gateway, CreateOrderParams
from apps.product.models import Product
from apps.payment.enums import PaymentMethod


class OrderView(GenericViewSet):
    lookup_field = 'order_id'

    def get_queryset(self):
        return Order.objects.filter(deleted_at__isnull=True)

    def create(self, request):
        serializer = CreateOrderSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)

        params = CreateOrderParams(
            product=serializer.validated_data.get('product'),
            quantity=serializer.validated_data.get('quantity'),
            payment_method=serializer.validated_data.get('payment_method'),
            order_destination=serializer.validated_data.get('order_destination'),
        )
        order = payment_gateway.make_payment(params)
        response = DetailOrderSerializer(order, context=self.get_serializer_context())
        return Response(response.data, status=status.HTTP_201_CREATED)
    
    def retrieve(self, request, order_id):
        order = self.get_object()
        serializer = DetailOrderSerializer(order, context=self.get_serializer_context())
        return Response(serializer.data)
    
    @action(methods=['post', 'get'], detail=False, permission_classes=())
    def stub(self, request):
        order = None
        if request.method == 'POST':
            order_id = request.data.get('order_id')
            product_id = request.data.get('product_id')
            payment_method = request.data.get('payment_method')
            product = Product.objects.filter(id=product_id).first()
            params = CreateOrderParams(
                product=product,
                quantity=1,
                payment_method=payment_method,
                order_destination=order_id,
            )
            order = payment_gateway.make_payment(params)
        elif request.method == 'GET':
            order_id = request.query_params.get('order_id')
            order = Order.objects.filter(order_id=order_id).first()
        if order is None:
            raise NotFound()
        serializer = DetailOrderSerializer(order, context=self.get_serializer_context())
        return Response(serializer.data)

class MidtransCallback(GenericViewSet):
    permission_classes = ()

    @action(methods=['post'], detail=True)
    def payment(self, request):
        if not payment_gateway.is_valid(request.data):
            raise ValidationError('Invalid signature')
        transaction_id = request.data.get('transaction_id')
        transaction = payment_gateway.get_transaction(transaction_id)
        order = Order.objects.filter(transaction_id=transaction_id).first()
        if order is None:
            raise NotFound()
        
        status = transaction.get('transaction_status')
        if status in ('settlement', 'capture'):
            order.status = OrderStatus.Success
            order.settlement_date = transaction.get('settlement_date')
            order.save()
        elif status in ('deny', 'expire'):
            order.status = OrderStatus.Failed
            order.save()
        elif status == 'cancel':
            order.status = OrderStatus.Cancel
            order.save()
        
        return Response()

order_view = OrderView
midtrans_callback_view = MidtransCallback
