from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[datetime] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    is_seller: bool = False
    is_admin: bool = False

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[datetime] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

