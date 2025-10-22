from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class NotificationBase(BaseModel):
    user_id: int
    message: str
    is_read: bool = False

class NotificationCreate(NotificationBase):
    pass

class Notification(NotificationBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
