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

class SellerInfoUpdate(BaseModel):
    shop_name: Optional[str] = None
    shop_address: Optional[str] = None
    shop_contact_number: Optional[str] = None
    business_permit: Optional[str] = None

class UserInDBBase(SellerInfoUpdate):
    id: int
    rating: float
    rating_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class User(UserBase):
    pass

class UserInDB(UserInDBBase):
    hashed_password: str

class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    shop_name: Optional[str] = None
    shop_address: Optional[str] = None
    shop_contact_number: Optional[str] = None
    is_seller: bool
    rating: float

    class Config:
        orm_mode = True

