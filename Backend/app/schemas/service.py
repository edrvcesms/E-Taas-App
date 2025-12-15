from pydantic import BaseModel
from typing import Optional

class ServiceBase(BaseModel):
    service_name: str
    owner_name: str
    service_contact: Optional[str] = None
    service_address: Optional[str] = None
    description: Optional[str] = None
    price_range: Optional[str] = None
    fb_link: Optional[str] = None
    is_available: Optional[bool] = True
    category_id: int

class ServiceCreate(ServiceBase):
    pass