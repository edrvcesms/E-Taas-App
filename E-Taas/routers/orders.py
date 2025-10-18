from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from schemas.order import OrderCreate, OrderSchema
from services.order import checkout_order, get_order_by_id, get_orders_by_user, cancel_order
from db.database import get_db
from dependencies.auth import current_user
from models import users as user_model
from typing import List

router = APIRouter(
    tags=["Orders"],
    prefix="/orders"
)

@router.post("/checkout", status_code=status.HTTP_201_CREATED, response_model=OrderSchema)
def checkout(order: OrderCreate, db: Session = Depends(get_db), user: user_model.User = Depends(current_user)):
    return checkout_order(db, user.id, order)

@router.get("/", response_model=List[OrderSchema])
def get_all_orders(db: Session = Depends(get_db), user: user_model.User = Depends(current_user)):
    return get_orders_by_user(db, user.id)

@router.get("/{order_id}", response_model=OrderSchema)
def get_single_order(order_id: int, db: Session = Depends(get_db), user: user_model.User = Depends(current_user)):
    return get_order_by_id(db, order_id, user.id)

@router.put("/{order_id}/cancel", response_model=OrderSchema)
def cancel_user_order(order_id: int, db: Session = Depends(get_db), user: user_model.User = Depends(current_user)):
    return cancel_order(db, order_id, "cancelled")
                        