from functools import lru_cache
from pydantic import BaseSettings, BaseModel

# get config from appsettings.json
# https://pydantic-docs.helpmanual.io/usage/settings/#adding-sources

class ServerSettings(BaseModel):
    SERVER_API_APP_NAME: str = 'defaultmq'
    SERVER_APP_VERSION: str = '0.0.0'
    SERVER_APP_DOCS_URL: str = '/swagger'

    SERVER_EXPOSE_PORT: int = 80
    SERVER_HOST: str = '0.0.0.0'
    SERVER_DEVELOPMENT: bool = False
    SERVER_WORKERS: int = 5
    SERVER_TIMEOUT: int = 10

    SERVER_LOG_LEVEL: str = "INFO"

    class Config:
        env_file = "config.env"

class DatabaseSettings(BaseModel):
    DB_CONNECTION_STRING: str = 'http://elasticsearch:9200'
    DB_ENGINE: str = 'ELASTICSEARCH'

    class Config:
        env_file = "config.env"

class ElasticAPMSettings(BaseModel):
    APM_ENABLED: bool = True
    APM_URL: str = 'http://apm-server:8200'
    APM_TOKEN: str = 'TOKEN1939'

    class Config:
        env_file = "config.env"


class CacheSettings(BaseModel):
    CACHE_ENGINE: str = 'REDIS'
    CACHE_URL: str = 'redis'
    CACHE_PORT: int = 6379
    CACHE_USER: str = "test"
    CACHE_PASSWORD: str = "test"
    
    class Config:
        env_file = "config.env"


@lru_cache()
class Settings(BaseSettings):

    server: ServerSettings = ServerSettings()
    db: DatabaseSettings = DatabaseSettings()
    elastic_apm: ElasticAPMSettings = ElasticAPMSettings()
    cache_settings = CacheSettings()
