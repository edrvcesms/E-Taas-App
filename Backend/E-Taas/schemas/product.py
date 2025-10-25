from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    base_price: float
    category_id: int


class VariantCategoryBase(BaseModel):
    product_id: int
    name: str  # e.g., "Size", "Color"
    values: str  # e.g., "S,M,L" or "Red,Blue"


class VariantBase(BaseModel):
    variant_combination: str
    variant_price: float
    stock_quantity: int
    image: Optional[str] = None



class ProductCreate(ProductBase):
    images: Optional[List[str]] = None
    variants: Optional[List[VariantBase]] = None

class ProductResponse(ProductCreate):
    id: int

    class Config:
        orm_mode = True