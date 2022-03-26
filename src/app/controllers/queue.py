from fastapi import APIRouter, HTTPException, Depends
from utils.exceptions import NotFoundInDatabase, UnauthorizedDbAccess
from database import db
from models.queue import Queue
from fastapi.security import HTTPBasic, HTTPBasicCredentials
# from utils.observability import logger

app = APIRouter()
security = HTTPBasic()

@app.post("/consumption/{queue}/", response_model=Queue)
async def consume_events(queue: str, consumer: str | None = "elasticmq", batch: int | None = 10, credentials: HTTPBasicCredentials = Depends(security)):
    try:
        result =  await db.consume_events((credentials.username, credentials.password), queue, consumer, batch)
    except NotFoundInDatabase:
        raise HTTPException(404)
    except UnauthorizedDbAccess:
        raise HTTPException(401)
        
    queue = Queue(events=result)
    return queue