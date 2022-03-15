from elasticsearch import Elasticsearch, NotFoundError
import redis
import json
from utils.observability import logger
from utils.exceptions import NotFoundInDatabase
redis = redis.Redis(host='redis', port=6379)

class ElasticsearchBackend():

    def _init_db_conn(self, auth):
        es = Elasticsearch(auth)
        return es

    async def db_check_connection(self) -> int:
        return 200
 
    async def _create_index(es, index):
        es.indices.create(index=index, ignore=400)

    async def create_event(self, auth, index, document):
        index = f'defaultmq-{index}'
        es = Elasticsearch(auth)
        es.indices.create(index=index, ignore=400)
        es.index(index=index, document=document)

    async def get_event(self, auth, index, document_id):
        index = f'defaultmq-{index}'
        es = Elasticsearch(auth)
        result = es.get(index=index, id=document_id)
        result = result["_source"]["message"]
        return result
    
    async def _update_events_statuses(self, auth, index, consumer, events, cache_key):
        es = Elasticsearch(auth)

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
        concurrent_consumption = json.loads(redis.get(cache_key))
        consumption_delta = list(set(concurrent_consumption).difference(set(events)))
        redis.set(cache_key, str(json.dumps(consumption_delta)), ex=60)

    async def _process_elastic_events_response(self, response, cache_key):
        events = []
        for hit in response['hits']['hits']:
            events.append(hit['_id'])
        if events == []:
            raise NotFoundInDatabase

        concurrent_consumption = redis.get(cache_key)

        if concurrent_consumption == None or concurrent_consumption == "[]": 
            redis.set(cache_key, str(json.dumps(events)), ex=60) 
        else:
            concurrent_consumption = list(json.loads(concurrent_consumption))
            merged_consumption = list(set(events + concurrent_consumption))
            events = list(set(events).difference(set(concurrent_consumption)))
            redis.set(cache_key, str(json.dumps(merged_consumption)), ex=60)

        return events


    async def consume_events(self, auth, index, consumer, batch):
        index = f'defaultmq-{index}'
        cache_key = f'{index}-{consumer}'
        es = Elasticsearch(auth)
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
    
        except NotFoundError:
            raise NotFoundInDatabase

        return events

