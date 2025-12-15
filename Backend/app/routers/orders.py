from typing import List
from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.orders import OrderCreate, OrderCreateCart
from services.orders import get_orders_by_user, create_new_order, get_order_by_id, cancel_order_by_id, mark_order_as_received, create_order_from_cart
from dependencies.auth import current_user
from dependencies.database import get_db
from dependencies.limiter import limiter

router = APIRouter()

@router.get("/", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_user_orders(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    orders = await get_orders_by_user(db, current_user.id)
    return orders

@router.get("/{order_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def get_order_details(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to view order details."
        )
    
    order = await get_order_by_id(db, order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found."
        )
    return order

@router.post("/checkout", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def checkout_order(
    request: Request,
    order: OrderCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to create an order."
        )
    
    new_order = await create_new_order(db, order, current_user.id)
    return new_order

@router.post("/checkout-cart", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def checkout_order_from_cart(
    request: Request,
    order: OrderCreateCart,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to create an order."
        )
    
    new_order = await create_order_from_cart(db, current_user.id, order)
    return new_order

@router.put("/cancel/{order_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def cancel_order(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to cancel an order."
        )
    
    canceled_order = await cancel_order_by_id(db, order_id, current_user.id)
    return canceled_order

@router.put("/mark-received/{order_id}", status_code=status.HTTP_200_OK)
@limiter.limit("5/minute")
async def mark_order_received(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(current_user)
):
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to mark an order as received."
        )
    
    received_order = await mark_order_as_received(db, order_id, current_user.id)
    return received_order
