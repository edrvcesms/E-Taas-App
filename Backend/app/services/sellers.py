from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
from app.models.sellers import Seller
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.sellers import SellerCreate
from typing import List
from app.utils.logger import logger
from app.models.orders import Order
from app.models.services import Service
from app.services.notification import create_new_notification
from app.schemas.sellers import SwitchRoleRequest
from app.models.users import User

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
            owner_address=seller_data.owner_address,
            is_verified=True,
            is_seller_mode=False
        )

        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )
        
        user.is_seller = True
        db.add(user)
        db.add(new_seller)
        await db.commit()
        await db.refresh(new_seller)


        return new_seller

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error in become_a_seller: {e}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

async def switch_role(db: AsyncSession, user_id: int, switch_role_request: SwitchRoleRequest) -> Seller:
    try:
        seller_result = await db.execute(select(Seller).where(Seller.user_id == user_id))
        seller = seller_result.scalar_one_or_none()

        if not seller:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Seller not found."
            )
        
        # if not seller.is_verified:
        #     raise HTTPException(
        #         status_code=status.HTTP_403_FORBIDDEN,
        #         detail="Seller is not verified. Cannot switch to seller mode."
        #     )

        seller.is_seller_mode = switch_role_request.is_seller_mode
        await db.commit()
        await db.refresh(seller)

        return seller

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error in switch_to_seller_mode: {e}")

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
        result = await db.execute(select(Order).options(selectinload(Order.seller)).where(Order.id == order_id))
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
        await create_new_notification(db, order.user_id, f"Your order from {order.seller.business_name} has been confirmed.", role="user")
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
    
async def get_revenue(db: AsyncSession, seller_id: int) -> float:
    try:
        result = await db.execute(
            select(Order).where(
                Order.seller_id == seller_id,
                Order.status == "Delivered"
            )
        )
        orders = result.scalars().all()
        total_revenue = sum(order.total_amount for order in orders)
        logger.info(f"Total revenue for seller_id {seller_id} is {total_revenue}")
        return total_revenue
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error calculating revenue for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate seller revenue."
        ) from e
    
async def get_total_orders_count(db: AsyncSession, seller_id: int) -> int:
    try:
        result = await db.execute(
            select(Order).where(Order.seller_id == seller_id)
        )
        orders = result.scalars().all()
        total_orders = len(orders)
        logger.info(f"Total orders count for seller_id {seller_id} is {total_orders}")
        return total_orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error calculating total orders count for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate total orders count."
        ) from e
    
async def get_pending_orders_count(db: AsyncSession, seller_id: int) -> int:
    try:
        result = await db.execute(
            select(Order).where(
                Order.seller_id == seller_id,
                Order.status == "Pending"
            )
        )
        orders = result.scalars().all()
        pending_orders = len(orders)
        logger.info(f"Pending orders count for seller_id {seller_id} is {pending_orders}")
        return pending_orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error calculating pending orders count for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate pending orders count."
        ) from e
    

async def get_shipped_orders_count(db: AsyncSession, seller_id: int) -> int:
    try:
        result = await db.execute(
            select(Order).where(
                Order.seller_id == seller_id,
                Order.status == "Shipped"
            )
        )
        orders = result.scalars().all()
        shipped_orders = len(orders)
        logger.info(f"Shipped orders count for seller_id {seller_id} is {shipped_orders}")
        return shipped_orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error calculating shipped orders count for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate shipped orders count."
        ) from e
    
async def get_delivered_orders_count(db: AsyncSession, seller_id: int) -> int:
    try:
        result = await db.execute(
            select(Order).where(
                Order.seller_id == seller_id,
                Order.status == "Delivered"
            )
        )
        orders = result.scalars().all()
        delivered_orders = len(orders)
        logger.info(f"Delivered orders count for seller_id {seller_id} is {delivered_orders}")
        return delivered_orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error calculating delivered orders count for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to calculate delivered orders count."
        ) from e
    
async def get_recent_orders(db: AsyncSession, seller_id: int, limit: int = 5) -> List[Order]:
    try:
        result = await db.execute(
            select(Order)
            .where(Order.seller_id == seller_id)
            .order_by(Order.created_at.desc())
            .limit(limit)
        )
        recent_orders = result.scalars().all()
        logger.info(f"Fetched {len(recent_orders)} recent orders for seller_id {seller_id}")
        return recent_orders
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching recent orders for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent orders."
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
        order.shipped_at = datetime.utcnow().isoformat()
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
    
async def get_recent_inquiries(db: AsyncSession, seller_id: int, limit: int = 5):
    try:
        result = await db.execute(
            select(Service)
            .where(Service.seller_id == seller_id)
            .order_by(Service.created_at.desc())
            .limit(limit)
        )
        recent_inquiries = result.scalars().all()
        logger.info(f"Fetched {len(recent_inquiries)} recent inquiries for seller_id {seller_id}")
        return recent_inquiries
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error fetching recent inquiries for seller_id {seller_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to fetch recent inquiries."
        ) from e