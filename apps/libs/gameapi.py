import random
from faker import Faker
from django.core.cache import cache

from apps.product.models import Game

faker = Faker()

class GameAPI:
    def check_account(self, game: Game, id, server_id):
        # haven't integrated yet, sorry
        if id + server_id == '4339100209952':
            return 'I am Lord Voldemort'
        return None

        cache_key = f'{game.id}-{id}{server_id}'
        cached_result = cache.get(cache_key)
        if cached_result:
            return cached_result

        username = faker.user_name()
        cache.set(cache_key, username, timeout=60 * 3)
        return username

game_api = GameAPI()
