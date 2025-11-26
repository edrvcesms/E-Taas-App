from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from models.sellers import Seller
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.sellers import SellerCreate
from typing import List
from utils.logger import logger
from models.orders import Order

async def become_a_seller(db: AsyncSession, seller_data: SellerCreate, user_id: int) -> Seller:
    try:
        seller = await db.execute(select(Seller).where(Seller.user_id == user_id))
        existing_seller = seller.scalar_one_or_none()
        if existing_seller:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User is already a seller."
            )
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authentication required to apply as a seller."
            )

        new_seller = Seller(
            user_id=user_id,
            business_name=seller_data.business_name,
            business_address=seller_data.business_address,
            business_contact=seller_data.business_contact,
            display_name=seller_data.display_name,
            owner_address=seller_data.owner_address
        )
        
        db.add(new_seller)
        await db.commit()
        await db.refresh(new_seller)


        return JSONResponse(
            status_code = status.HTTP_201_CREATED,
            content={
                "message": "Seller application successful",
                "seller_id": new_seller.id,
                "is_verified": new_seller.is_verified
            }
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error in become_a_seller: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
async def get_shop_details(db: AsyncSession, user_id: int) -> Seller:
    try:
        seller_result = await db.execute(select(Seller).where(Seller.user_id == user_id))
        seller = seller_result.scalar_one_or_none()

        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller shop not found."
            )

        return seller

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error in get_shop_details: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

async def get_all_orders_by_seller(db: AsyncSession, seller_id: int) -> List[Order]:
    try:
        result = await db.execute(select(Order).where(Order.seller_id == seller_id, Order.status == "Pending"))
        logger.info(f"Fetched orders for seller_id {seller_id}")
        orders = result.scalars().all()
        logger.info(f"Orders: {orders}")
        if not orders:
            return []
        return orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching orders for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch orders for the seller."
        ) from e
    
async def confirm_order_by_id(db: AsyncSession, order_id: int, seller_id: int) -> Order:
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order.seller_id != seller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to confirm this order."
            )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        if order.status != "Pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only pending orders can be confirmed."
            )
        
        order.status = "Confirmed"
        await db.commit()
        await db.refresh(order)
        logger.info(f"Order ID {order_id} confirmed.")

        return order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error confirming order ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to confirm the order."
        ) from e
    
async def send_shipping_link(db: AsyncSession, order_id: int, shipping_link: str, seller_id: int) -> Order:
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order.seller_id != seller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this order."
            )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        if order.status != "Confirmed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only confirmed orders can be shipped."
            )
        
        order.shipping_link = shipping_link
        order.status = "Shipped"
        await db.commit()
        await db.refresh(order)
        logger.info(f"Shipping link for Order ID {order_id} updated.")

        return order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error updating shipping link for Order ID {order_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update the shipping link."
        ) from e
    
async def mark_order_as_delivered(db: AsyncSession, order_id: int, seller_id: int) -> Order:
    try:
        result = await db.execute(select(Order).where(Order.id == order_id))
        order = result.scalar_one_or_none()
        if order.seller_id != seller_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to update this order."
            )
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Order not found."
            )
        if order.status != "Shipped":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only shipped orders can be marked as delivered."
            )
        
        order.status = "Delivered"
        await db.commit()
        await db.refresh(order)
        logger.info(f"Order ID {order_id} marked as delivered.")

        return order

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.error(f"Error marking Order ID {order_id} as delivered: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to mark the order as delivered."
        ) from e