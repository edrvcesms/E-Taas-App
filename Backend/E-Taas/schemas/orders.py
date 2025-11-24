from pydantic import BaseModel
from typing import List, Optional

class OrderItemBase(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderBase(BaseModel):
    shipping_address: str
    payment_method: str
    order_items: List[OrderItemCreate]

class OrderCreate(OrderBase):
    user_id: int
    seller_id: int
    