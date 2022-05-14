from elasticsearch import Elasticsearch, NotFoundError, AuthenticationException
import redis
import json
# from utils.observability import logger
from utils.exceptions import NotFoundInDatabase, UnauthorizedDbAccess
from config import config
cache = redis.Redis(host='redis', port=6379)

class ElasticsearchBackend():

    def __init__(self) -> None:
        pass
    # def __init__(self, server_name, connection_string):
    #     self.server_name = server_name
    #     self.connection_string = connection_string


    def _init_db_conn(self, auth):
        es = Elasticsearch(config.db.DB_CONNECTION_STRING, http_auth=auth)
        return es


    async def _create_final_index_name(slef, index) -> str:
        return f'{config.server.SERVER_API_APP_NAME}-{index}'.lower()


    async def _update_events_statuses(self, auth, index, consumer, events, cache_key):
        es = self._init_db_conn(auth)

        es.update_by_query(
            index=index,
            body={ 
                "script": {
                    "inline": "ctx._source.consumed_by.addAll(params.val)",
                    "lang": "painless",
                    "params": {
                    "val": [consumer]
                    }
                },
                "query": {
                    "ids" : {
                    "values" : events
                    }
                }
            },
            wait_for_completion = True,
            refresh=True
        )
        concurrent_consumption = json.loads(cache.get(cache_key))
        consumption_delta = list(set(concurrent_consumption).difference(set(events)))
        cache.set(cache_key, str(json.dumps(consumption_delta)), ex=60)
        del es


    async def _process_elastic_events_response(self, response, cache_key):
        events = []
        for hit in response['hits']['hits']:
            events.append(hit['_id'])
        if events == []:
            raise NotFoundInDatabase

        concurrent_consumption = cache.get(cache_key)

        if concurrent_consumption == None or concurrent_consumption == "[]": 
            cache.set(cache_key, str(json.dumps(events)), ex=60) 
        else:
            concurrent_consumption = list(json.loads(concurrent_consumption))
            merged_consumption = list(set(events + concurrent_consumption))
            events = list(set(events).difference(set(concurrent_consumption)))
            cache.set(cache_key, str(json.dumps(merged_consumption)), ex=60)

        return events
        

    async def create_event(self, auth, index, document):
        index = await self._create_final_index_name(index)

        try: 
            es = self._init_db_conn(auth)
            es.index(index=index, document=document, ignore=400)
            del es
        except AuthenticationException:
            raise UnauthorizedDbAccess


    async def get_event(self, auth, index, document_id):
        index = await self._create_final_index_name(index)

        try:
            es = self._init_db_conn(auth)
            result = es.get(index=index, id=document_id)
            del es
        except AuthenticationException:
            raise UnauthorizedDbAccess

        result = result["_source"]["message"]
        return result


    async def consume_events(self, auth, index, consumer, batch):
        index = await self._create_final_index_name(index)
        cache_key = f'{index}-{consumer}'
        es = Elasticsearch(config.db.DB_CONNECTION_STRING, http_auth=auth)
        try: 
            response = es.search(
                index=index,
                body={
                    "query": {
                        "bool": {
                            "must_not": [
                                {
                                    "term": {
                                        "consumed_by": {
                                            "value": consumer
                                        }
                                    }
                                }
                            ]
                        }
                    },
                    "sort": { "timestamp": "asc"},
                    "size": batch,
                    "_source": "false"
                }
            )
            events = await self._process_elastic_events_response(response, cache_key)
            await self._update_events_statuses(auth, index, consumer, events, cache_key)
            del es
    
        except NotFoundError:
            raise NotFoundInDatabase

        except AuthenticationException:
            raise UnauthorizedDbAccess

        return events

