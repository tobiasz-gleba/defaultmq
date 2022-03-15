import logging
from config import config
from elasticapm.contrib.starlette import make_apm_client

logger = logging.getLogger("uvicorn.app")
if config.server.SERVER_DEVELOPMENT is True:
    logger.setLevel(logging.DEBUG)
    for handler in logger.handlers:
        handler.setLevel(logging.DEBUG)


apm = make_apm_client({
    'SERVER_URL': config.elastic_apm.APM_URL,
    'SERVICE_NAME': config.server.SERVER_API_APP_NAME,
    'SECRET_TOKEN': config.elastic_apm.APM_TOKEN,
    'CAPTURE_HEADERS': config.server.SERVER_DEVELOPMENT,
    'DEBUG': config.server.SERVER_DEVELOPMENT,
    'LOG_ECS_REFORMATTING': "override",
})