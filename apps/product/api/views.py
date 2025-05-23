from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action

from apps.product.models import Game, Product


class GameView(GenericViewSet):
    permission_classes = ()

    def get_queryset(self):
        return Game.objects.filter(deleted_at__isnull=True).values('id', 'name').order_by('name')

    def list(self, request):
        queryset = self.get_queryset()
        return Response(queryset)
    
    @action(methods=['get'], detail=True)
    def products(self, request, pk):
        products = Product.objects.filter(deleted_at__isnull=True, game_id=pk).values('id', 'name', 'price').order_by('price')
        return Response(products)

game_view = GameView
