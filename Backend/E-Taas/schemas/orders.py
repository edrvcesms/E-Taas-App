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
    

class OrderItemResponse(BaseModel):
    product_id: int
    variant_id: Optional[int] = None
    quantity: int
    price: float

class OrderResponse(BaseModel):
    id: int
    user_id: int
    seller_id: int
    total_amount: float
    shipping_address: str
    status: str
    payment_status: str
    payment_method: str
    order_reference: str
    shipping_fee: float
    created_at: str
    order_items: List[OrderItemResponse]

    class Config:
        orm_mode = True