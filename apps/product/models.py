from django.db import models

from apps.utils.models import BaseModel


class Game(BaseModel):
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Product(BaseModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, db_index=True, unique=True)
    game = models.ForeignKey(Game, on_delete=models.PROTECT, related_name='products')
    price = models.IntegerField()

    def __str__(self):
        return self.name
