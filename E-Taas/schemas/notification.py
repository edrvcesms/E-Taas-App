from pydantic import BaseModel
from datetime import datetime

class NotificationBase(BaseModel):
    message: str
    is_read: bool = False
    created_at: datetime

    class Config:
        orm_mode = True

class UserNotificationResponse(NotificationBase):
    id: int
    user_id: int


class SellerNotificationResponse(NotificationBase):
    id: int
    user_id: int

class Notification(NotificationBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True
