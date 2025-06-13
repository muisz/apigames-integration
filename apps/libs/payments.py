import secrets
import requests
import base64
import hashlib
from django.conf import settings

from apps.order.enums import OrderStatus
from apps.order.models import Order
from apps.product.models import Product
from apps.payment.enums import PaymentMethod


class PaymentError(Exception):
    pass

class CreateOrderParams:
    product: Product
    quantity: int
    payment_method: int
    order_destination: str

    def __init__(self, product: Product, quantity: int, payment_method: int, order_destination: str):
        self.product = product
        self.quantity = quantity
        self.payment_method = payment_method
        self.order_destination = order_destination
    
    @property
    def code(self):
        return self.product.code
    
    @property
    def name(self):
        return self.product.name

    @property
    def amount(self):
        return self.product.price * self.quantity

class MidtransPayment:
    IS_PRODUCTION = settings.MIDTRANS_IS_PRODUCTION
    CLIENT_ID = settings.MIDTRANS_CLIENT_ID
    SERVER_KEY = settings.MIDTRANS_SERVER_KEY

    def is_valid(self, payload: dict):
        order_id = payload.get('order_id')
        status_code = payload.get('status_code')
        gross_amount = payload.get('gross_amount')
        key = f'{order_id}{status_code}{gross_amount}{self.SERVER_KEY}'
        return hashlib.sha512(key.encode()).hexdigest() == payload.get('signature_key')
    
    def get_transaction(self, id: str):
        url = f'{self._get_host()}/v2/{id}/status'
        headers = {'Authorization': f'Basic {self._get_basic_token()}'}
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise PaymentError(f'Failed to get transaction status: {response.content}')
        return response.json()

    def make_payment(self, params: CreateOrderParams):
        if params.payment_method == PaymentMethod.VA_BNI:
            return self._create_va_bni(params)
        elif params.payment_method == PaymentMethod.VA_BCA:
            return self._create_va_bca(params)
        raise PaymentError('No payment method selected')
    
    def _create_va_bni(self, params: CreateOrderParams):
        url = f'{self._get_host()}/v2/charge'
        headers = {'Authorization': f'Basic {self._get_basic_token()}'}
        payload = {
            'payment_type': 'bank_transfer',
            'transaction_details': {
                'order_id': secrets.token_hex(16),
                'gross_amount': params.amount,
            },
            'bank_transfer': {
                'bank': 'bni',
            },
            'item_details': [
                {
                    'id': params.code,
                    'price': params.product.price,
                    'quantity': params.quantity,
                    'name': params.name,
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise PaymentError(f'Failed to create VA BNI: {response.content}')
        json_response = response.json()
        status_code = json_response.get('status_code')
        if status_code != '201':
            raise PaymentError(f'Failed to create VA BNI: {json_response}')
        transaction_id = json_response.get('transaction_id')
        va = json_response['va_numbers'][0]['va_number']
        return Order.objects.create(
            name=params.name,
            product=params.product,
            quantity=params.quantity,
            amount=params.amount,
            payment_method=params.payment_method,
            status=OrderStatus.Pending,
            order_id=payload['transaction_details']['order_id'],
            transaction_id=transaction_id,
            virtual_account=va,
            order_destination=params.order_destination,
        )

    def _create_va_bca(self, params: CreateOrderParams):
        url = f'{self._get_host()}/v2/charge'
        headers = {'Authorization': f'Basic {self._get_basic_token()}'}
        payload = {
            'payment_type': 'bank_transfer',
            'transaction_details': {
                'order_id': secrets.token_hex(16),
                'gross_amount': params.amount,
            },
            'bank_transfer': {
                'bank': 'bca',
            },
            'item_details': [
                {
                    'id': params.code,
                    'price': params.product.price,
                    'quantity': params.quantity,
                    'name': params.name,
                }
            ]
        }
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise PaymentError(f'Failed to create VA BCA: {response.content}')
        json_response = response.json()
        print(json_response)
        print(url)
        status_code = json_response.get('status_code')
        if status_code != '201':
            raise PaymentError(f'Failed to create VA BCA: {json_response}')
        transaction_id = json_response.get('transaction_id')
        va = json_response['va_numbers'][0]['va_number']
        return Order.objects.create(
            name=params.name,
            product=params.product,
            quantity=params.quantity,
            amount=params.amount,
            payment_method=params.payment_method,
            status=OrderStatus.Pending,
            order_id=payload['transaction_details']['order_id'],
            transaction_id=transaction_id,
            virtual_account=va,
            order_destination=params.order_destination,
        )
    
    def _get_host(self):
        if self.IS_PRODUCTION:
            return 'https://api.midtrans.com'
        return 'https://api.sandbox.midtrans.com'
    
    def _get_basic_token(self):
        return base64.b64encode(f'{self.SERVER_KEY}:'.encode()).decode()

payment_gateway = MidtransPayment()
