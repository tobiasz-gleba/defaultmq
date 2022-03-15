# from models.event import Event
from fastapi import APIRouter, HTTPException
from utils.exceptions import NotFoundInDatabase
from database import db
from models.queue import Queue
from utils.observability import logger

app = APIRouter()

@app.post("/consumption/{queue}/", response_model=Queue)
async def consume_events(queue: str, consumer: str | None = "elasticmq", batch: int | None = 10):
    try:
        result =  await db.consume_events("http://elasticsearch:9200", queue, consumer, batch)
    except NotFoundInDatabase:
        raise HTTPException(404)
        
    queue = Queue(events=result)
    return queue

