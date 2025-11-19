from fastapi import HTTPException, status, APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from services.sellers import become_a_seller, get_shop_details
from services.products import add_product_service, update_product_service, add_variant_categories_with_attributes, add_product_variants, update_variant_category_service, update_variant_service
from dependencies.database import get_db
from dependencies.auth import current_user
from schemas.sellers import SellerCreate
from schemas.product import ProductFullCreate, ProductFullUpdate
import logging
from dependencies.limiter import limiter
from models.users import User

router = APIRouter()

logger = logging.getLogger(__name__)

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


@router.get("/shop", status_code=status.HTTP_200_OK)
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


@router.post("/add-product", status_code=status.HTTP_201_CREATED)
@limiter.limit("10/minute")
async def add_product_route(
    request: Request,
    data: ProductFullCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can add products."
        )

    product = await add_product_service(db, data.product, current_user.id)

    if data.product.has_variants:
        if not data.variant_categories or not data.variants:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Variant categories and variants are required."
            )

        await add_variant_categories_with_attributes(db, data.variant_categories, product.id)

        await add_product_variants(db, data.variants, product.id)

    return product


@router.put("/update-product/{product_id}", status_code=status.HTTP_200_OK)
@limiter.limit("10/minute")
async def update_product(
    request: Request,
    product_id: int,
    data: ProductFullUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(current_user)
):
    if not current_user or not current_user.is_seller:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only sellers can update products."
        )

    product = await update_product_service(db, product_id, data.product)

    if data.variants:
        for var_data in data.variants:
            await update_variant_service(db, var_data.id, var_data)

    if data.variant_categories:
        for cat_data in data.variant_categories:
            await update_variant_category_service(db, cat_data)

    return product