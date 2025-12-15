from pydantic import BaseModel
from typing import List, Optional

class MessageCreate(BaseModel):
    receiver_id: int
    sender_type: str
    message: Optional[str] = None