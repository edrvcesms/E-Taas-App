from pydantic import BaseModel
from typing import Optional, List

class ProductBase(BaseModel):
    product_name: str
    description: Optional[str] = None
    base_price: float
    stock: int
    has_variants: bool = False
    category_id: int

class ProductCreate(ProductBase):
    seller_id: int

class ProductUpdate(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    stock: Optional[int] = None
    has_variants: Optional[bool] = None
    category_id: Optional[int] = None


class VariantBase(BaseModel):
    stock: int
    price: float
    image_url: str


class VariantCreate(VariantBase):
    pass


class VariantAttributeCreate(BaseModel):
    value: str

class VariantCategoryCreate(BaseModel):
    category_name: str
    attributes: Optional[List[VariantAttributeCreate]] = None


class ProductFullCreate(BaseModel):
    product: ProductCreate
    variant_categories: Optional[List[VariantCategoryCreate]] = None
    variants: Optional[List[VariantCreate]] = None


