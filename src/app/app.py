import asyncio
import uvicorn

from config import config
from core.core import app_core
from core.cron import hello

# server startup conf
server_config = uvicorn.Config(
    app=app_core,
    host=config.server.SERVER_HOST,
    port=config.server.SERVER_EXPOSE_PORT,
    reload=config.server.SERVER_DEVELOPMENT,
    debug=config.server.SERVER_DEVELOPMENT,
    workers=config.server.SERVER_WORKERS,
    timeout_keep_alive=config.server.SERVER_TIMEOUT,
    access_log=config.server.SERVER_DEVELOPMENT,
    log_config="config/log_conf.yaml"
)
server = uvicorn.Server(server_config)

async def main():
    await asyncio.gather(server.serve(), hello())
    # server_run = asyncio.create_task(server.serve())
    # cron_watcher = asyncio.create_task(hello())
    # await server_run
    # await cron_watcher

# fastapi start async loop
if __name__ == "__main__":
    asyncio.run(main())
