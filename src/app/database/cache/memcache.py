from random import expovariate
from config import config
from memcache import Client
#TODO implement memcached

class MemcacheCache():
    
    def __init__(self):
        self.connection = Client([f'{config.cache_settings.CACHE_URL}:{config.cache_settings.CACHE_PORT}'])

    def get(self, cache_key):
        self.connection.get(cache_key)

    def set(self, cache_key, value, expire=-1):
        self.connection.set(cache_key, value, expire)
