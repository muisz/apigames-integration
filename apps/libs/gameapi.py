import random
from faker import Faker
from django.core.cache import cache

from apps.product.models import Game

faker = Faker()

class GameAPI:
    def check_account(self, game: Game, id, server_id):
        cache_key = f'{game.id}-{id}{server_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        username = faker.user_name()
        cache.set(cache_key, username, timeout=60 * 3)
        return username

game_api = GameAPI()
