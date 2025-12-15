from pydantic import BaseModel
from typing import Optional

class CartBase(BaseModel):
    user_id: int

class CartItemBase(BaseModel):
    variant_id: Optional[int] = None
    product_id: int
    quantity: int

