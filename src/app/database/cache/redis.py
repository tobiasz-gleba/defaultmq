from redis import Redis
from config import config
class RedisCache():
    
    def __init__(self):
        self.connection = Redis(host=config.cache_settings.CACHE_URL, port=config.cache_settings.CACHE_PORT)

    def get(self, cache_key):
        self.connection.get(cache_key)

    def set(self, cache_key, value, ex=-1):
        self.connection.set(cache_key, value, ex=ex)