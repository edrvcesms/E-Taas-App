from pydantic import BaseModel, EmailStr
from datetime import datetime

class SellerBase(BaseModel):
    business_name: str
    business_address: str
    business_contact: str
    display_name: str
    owner_address: str

class SellerCreate(SellerBase):
    pass

class PublicSeller(SellerBase):
    followers: int
    ratings: float

    class Config:
        orm_mode = True

class SwitchRoleRequest(BaseModel):
    is_seller_mode: bool