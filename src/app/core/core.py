from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from elasticapm.contrib.starlette import ElasticAPM
from config import config
from controllers.healthchecks import app as healthchecks
from controllers.event import app as events
from controllers.queue import app as queues
from utils.observability import apm

fast_api_args = {
    'title': config.server.SERVER_API_APP_NAME,
    'description': "Defaultmq is REST based message queue witch any database as a storage.",
    'version': config.server.SERVER_APP_VERSION,
    'docs_url': config.server.SERVER_APP_DOCS_URL,
}

# main instance of webserver
app_core = FastAPI(**fast_api_args)

if config.elastic_apm.APM_ENABLED:
    app_core.add_middleware(
        ElasticAPM, 
        client=apm
    )


app_core.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['GET','PUT','POST', 'DELETE', 'PATCH'],
    allow_headers=["*"],
)

app_core.include_router(events, prefix="/event", tags=["event"])
app_core.include_router(queues, prefix="/queues", tags=["queues"])
app_core.include_router(healthchecks, prefix="/healthcheck", tags=["healthcheck"])
