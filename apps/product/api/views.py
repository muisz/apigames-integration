from django.db.models.query import QuerySet
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound

from apps.product.api.serializers import CheckAccountSerializer
from apps.product.models import Game, Product
from apps.libs.gameapi import game_api


class GameView(GenericViewSet):
    permission_classes = ()

    def get_queryset(self):
        return Game.objects.filter(deleted_at__isnull=True).order_by('id')

    def list(self, request):
        queryset = self.get_queryset().values('id', 'name', 'image')
        return Response(queryset)
    
    @action(methods=['get'], detail=True)
    def products(self, request, pk):
        products = Product.objects.filter(deleted_at__isnull=True, game_id=pk).values('id', 'name', 'price').order_by('price')
        return Response(products)
    
    @action(methods=['post'], detail=True, url_path='check-account')
    def check_account(self, request, pk):
        game = self.get_object()
        serializer = CheckAccountSerializer(data=request.data, context=self.get_serializer_context())
        serializer.is_valid(raise_exception=True)
        username = game_api.check_account(
            game=game,
            id=serializer.validated_data.get('id'),
            server_id=serializer.validated_data.get('server_id'),
        )
        if not username:
            raise NotFound()
        return Response({'username': username})

game_view = GameView
