from pydantic import BaseModel

class Queue(BaseModel):
    events: list