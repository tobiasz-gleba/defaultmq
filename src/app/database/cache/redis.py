from redis import Redis
from config import config
class RedisCache():
    
    def __init__(self):
        self.connection = Redis(host=config.cache_settings.URL, port=config.cache_settings.PORT)

    def get(self, cache_key):
        self.connection.get(cache_key)

    def set(self, cache_key):
        self.connection.set(cache_key)
