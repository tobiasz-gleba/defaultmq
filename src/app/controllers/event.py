from models.event import Event
from fastapi import APIRouter, Body
from database import db
import json
from utils.observability import logger


app = APIRouter()

@app.post("/{queue}")
async def post_event(queue: str, payload: dict = Body(...)):
    event = Event(message=json.dumps(payload))
    await db.create_event(auth="http://elasticsearch:9200", index=queue, document=event.json())
    return {"accepted": "true"}


@app.get("/{queue}/{event_id}")
async def get_event(queue: str, event_id: str):
    result =  await db.get_event("http://elasticsearch:9200", queue, event_id)
    return result