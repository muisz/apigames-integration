from rest_framework.routers import DefaultRouter

from apps.product.api import views

app_name = 'api.product'
urlpatterns = []

router = DefaultRouter()
router.register('games', views.game_view, basename='game')

urlpatterns += router.urls
