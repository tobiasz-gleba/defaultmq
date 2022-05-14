from config import config
from memcache import Client

class MemcacheCache():
    
    def __init__(self):
        self.connection = Client([f'{config.cache_settings.URL}:{config.cache_settings.PORT}'])

    def get(self, cache_key):
        self.connection.get(cache_key)

    def set(self, cache_key):
        self.connection.set(cache_key)
