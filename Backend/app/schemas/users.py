from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from datetime import date
from app.schemas.sellers import PublicSeller

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None
    is_seller: bool = False
    is_admin: bool = False
    seller: Optional[PublicSeller] = None  # To include seller details if applicable
    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    birthdate: Optional[date] = None
    address: Optional[str] = None
    contact_number: Optional[str] = None

