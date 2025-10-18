from pydantic import BaseModel
from typing import Optional, List
from fastapi import UploadFile
from datetime import datetime


class ProductCreate(BaseModel):
    product_name: str
    price: float
    description: str
    stock: int = 0
    category_id: int

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    price: Optional[float] = None
    description: Optional[str] = None
    stock: Optional[int] = None
    image_url: Optional[str] = None
    category_id: Optional[int] = None

class ImageResponse(BaseModel):
    id: int
    product_id: int
    image_url: str

    class Config:
        orm_mode = True

class ProductResponse(BaseModel):
    id: int
    product_name: str
    price: float
    description: Optional[str]
    stock: int
    images: List[ImageResponse]
    category_id: int
    seller_id: int
    created_at: datetime
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True