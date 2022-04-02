from database.elasticsearch import ElasticsearchBackend
from utils.object_factory import ObjectFactory
from config import config

db_factory = ObjectFactory()
db_factory.register_builder('ELASTICSEARCH', ElasticsearchBackend)

db = db_factory.create(config.db.DB_ENGINE)