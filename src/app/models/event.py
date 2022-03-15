from pydantic import BaseModel, Json
from typing import Optional
from datetime import datetime

class Event(BaseModel):
    message: Json
    consumed_by: list = ['default']
    timestamp: Optional[datetime] = datetime.utcnow().isoformat()
    # allowed_to_consume: list = ['default']
    # deletion_timestamp: Optional[datetime]
    # post_adresses: Optional[list]
