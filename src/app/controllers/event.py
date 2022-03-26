from models.event import Event
from fastapi import APIRouter, Body, Depends, HTTPException
from database import db
import json
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from utils.exceptions import UnauthorizedDbAccess


app = APIRouter()
security = HTTPBasic()

@app.post("/{queue}")
async def post_event(queue: str, payload: dict = Body(...), credentials: HTTPBasicCredentials = Depends(security)):
    event = Event(message=json.dumps(payload))
    try: 
        await db.create_event(auth=(credentials.username, credentials.password), 
            index=queue, 
            document=event.json())
    except UnauthorizedDbAccess:
        raise HTTPException(401)

    return {"accepted": "true"}


@app.get("/{queue}/{event_id}")
async def get_event(queue: str, event_id: str, credentials: HTTPBasicCredentials = Depends(security)):
    try: 
        result =  await db.get_event((credentials.username, credentials.password), queue, event_id)
    except UnauthorizedDbAccess:
        raise HTTPException(401)
    
    return result
