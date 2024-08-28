from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional

from app.enum import TaskStatus


class TaskResponse(BaseModel):
    status: TaskStatus
    create_time: datetime
    start_time: Optional[datetime]
    time_to_execute: Optional[timedelta]
