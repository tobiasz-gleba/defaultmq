from database.cache.redis import RedisCache
from database.cache.memcache import MemcacheCache
from utils.object_factory import ObjectFactory
from config import config

cache_factory = ObjectFactory()
cache_factory.register_builder('REDIS', RedisCache)
cache_factory.register_builder('MEMCACHE', MemcacheCache)

cache = cache_factory.create(config.cache_settings.CACHE_ENGINE)