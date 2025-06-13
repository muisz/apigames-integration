from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from apps.payment.enums import PaymentMethod


class ListPaymentMethod(ListAPIView):
    def list(self, request):
        payment_methods = [{'id': enum[0], 'name': enum[1]} for enum in PaymentMethod.CHOICES]
        return Response(payment_methods)

list_payment_method = ListPaymentMethod.as_view()
