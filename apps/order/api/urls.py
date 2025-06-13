from rest_framework.routers import DefaultRouter

from apps.order.api import views

app_name = 'api.order'
urlpatterns = []

router = DefaultRouter()
router.register('orders', views.order_view, basename='order')
router.register('callbacks/midtrans', views.midtrans_callback_view, basename='midtrans-callback')

urlpatterns += router.urls
