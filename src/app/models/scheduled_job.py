from pydantic import BaseModel, Json
from typing import Optional

class ScheduledJob(BaseModel):
    queue_name: str
    timestamp: Optional[datetime] = datetime.utcnow().isoformat()
    last_execution_timestamp: Optional[datetime] = datetime.utcnow().isoformat()
    cron: str
    message: Json
