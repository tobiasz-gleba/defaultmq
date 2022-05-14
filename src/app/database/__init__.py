from database.engines.elasticsearch import ElasticsearchBackend
from utils.object_factory import ObjectFactory
from config import config

db_factory = ObjectFactory()
db_factory.register_builder('ELASTICSEARCH', ElasticsearchBackend)
db_factory.register_builder('CASSANDRA', ElasticsearchBackend)
db_factory.register_builder('MONGODB', ElasticsearchBackend)
db_factory.register_builder('MARIADB', ElasticsearchBackend)
db_factory.register_builder('POSTGRESS', ElasticsearchBackend)

db = db_factory.create(config.db.DB_ENGINE)