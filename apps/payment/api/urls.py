from django.urls import path

from apps.payment.api import views

app_name = 'api.payment'
urlpatterns = [
    path('payments/', views.list_payment_method, name='payments'),
]
