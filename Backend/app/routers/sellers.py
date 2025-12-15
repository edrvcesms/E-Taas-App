from fastapi import HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.sellers import become_a_seller, get_shop_details, get_all_orders_by_seller, confirm_order_by_id, send_shipping_link, mark_order_as_delivered, get_delivered_orders_count, get_pending_orders_count, get_recent_inquiries, get_recent_orders, get_revenue, get_total_orders_count, get_shipped_orders_count
from services.products import get_products_by_seller
from dependencies.database import get_db
from dependencies.auth import current_user
from schemas.sellers import SellerCreate
from dependencies.limiter import limiter
from models.users import User

router = APIRouter()


@router.post("/apply", status_code=status.HTTP_201_CREATED)
@limiter.limit("5/minute")
async def apply_as_seller(
    request: Request,
    seller_data: SellerCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    """Endpoint for users to apply as sellers."""
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required to apply as a seller."
        )
    if current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User is already a seller."
        )
    
    
    return await become_a_seller(db, seller_data, current_user.id)

@router.post("/send-shipping-link/{order_id}", status_code=status.HTTP_200_OK)
async def send_shipping_link_endpoint(
    request: Request,
    order_id: int,
    shipping_link: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can send shipping links."
        )
    
    response = await send_shipping_link(db, order_id, shipping_link, current_user.seller.id)
    return response


@router.get("/shop-details", status_code=status.HTTP_200_OK)
async def get_seller_shop(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user and not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can access their shop."
        )
    
    return await get_shop_details(db, current_user.id)

@router.get("/dashboard-metrics", status_code=status.HTTP_200_OK)
async def get_seller_dashboard_metrics(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can access dashboard metrics."
        )
    
    seller_id = current_user.seller.id

    total_revenue = await get_revenue(db, seller_id)
    total_orders = await get_total_orders_count(db, seller_id)
    pending_orders = await get_pending_orders_count(db, seller_id)
    shipped_orders = await get_shipped_orders_count(db, seller_id)
    delivered_orders = await get_delivered_orders_count(db, seller_id)
    recent_orders = await get_recent_orders(db, seller_id)
    recent_inquiries = await get_recent_inquiries(db, seller_id)

    return {
        "total_revenue": total_revenue,
        "total_orders": total_orders,
        "pending_orders": pending_orders,
        "shipped_orders": shipped_orders,
        "delivered_orders": delivered_orders,
        "recent_orders": recent_orders,
        "recent_inquiries": recent_inquiries
    }


@router.get("/my-products", status_code=status.HTTP_200_OK)
async def get_my_products(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can access their products."
        )
    
    products = await get_products_by_seller(db, current_user.seller.id)
    return products

@router.get("/orders", status_code=status.HTTP_200_OK)
async def get_seller_orders(
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can access their orders."
        )
    
    orders = await get_all_orders_by_seller(db, current_user.seller.id)
    return orders

@router.put("/confirm-order/{order_id}", status_code=status.HTTP_200_OK)
async def confirm_seller_order(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can confirm orders."
        )
    
    confirmation = await confirm_order_by_id(db, order_id, current_user.seller.id)
    return confirmation


@router.put("/mark-delivered/{order_id}", status_code=status.HTTP_200_OK)
async def mark_order_delivered_endpoint(
    request: Request,
    order_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can mark orders as delivered."
        )
    
    response = await mark_order_as_delivered(db, order_id, current_user.seller.id)
    return response