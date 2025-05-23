from django.contrib import admin

from apps.product.models import Game, Product


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_deleted', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'code', 'game', 'is_deleted', 'created_at')
    search_fields = ('name', 'code')
    autocomplete_fields = ('game',)
