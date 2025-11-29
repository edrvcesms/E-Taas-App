from pydantic import BaseModel
from typing import List, Optional

class MessageCreate(BaseModel):
    target_id: int
    sender: str  # 'user' or 'seller'
    conversation_id: int
    message: Optional[str] = None