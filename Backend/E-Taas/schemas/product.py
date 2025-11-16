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
    product_id: int
    attribute_ids: list[int]

class VariantCategoryCreate(BaseModel):
    product_id: int
    category_name: str

class VariantAttributeCreate(BaseModel):
    category_id: int
    value: str

class ProductFullCreate(BaseModel):
    product: ProductCreate
    variant_categories: Optional[List[VariantCategoryCreate]] = None
    variant_attributes: Optional[List[VariantAttributeCreate]] = None
    variants: Optional[List[VariantCreate]] = None


