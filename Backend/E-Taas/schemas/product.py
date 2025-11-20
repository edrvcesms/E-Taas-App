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

class VariantBase(BaseModel):
    stock: Optional[int] = 0
    price: Optional[float] = 0.0

class VariantCreate(VariantBase):
    pass

class VariantUpdate(VariantBase):
    id: Optional[int] = None

class UpdateProduct(BaseModel):
    product_name: Optional[str] = None
    description: Optional[str] = None
    base_price: Optional[float] = None
    stock: Optional[int] = None
    has_variants: Optional[bool] = None
    category_id: Optional[int] = None

class VariantAttributeCreate(BaseModel):
    id: Optional[int] = None  
    value: Optional[str] = None

class VariantCategoryCreate(BaseModel):
    category_name: Optional[str] = None
    attributes: Optional[List[VariantAttributeCreate]] = None

class UpdateVariantCategory(BaseModel):
    id: int
    category_name: Optional[str] = None
    attributes: Optional[List[VariantAttributeCreate]] = None

class ProductFullCreate(BaseModel):
    product: ProductCreate
    variant_categories: Optional[List[VariantCategoryCreate]] = None
    variants: Optional[List[VariantCreate]] = None

class ProductFullUpdate(BaseModel):
    product: UpdateProduct
    variant_categories: Optional[List[UpdateVariantCategory]] = None