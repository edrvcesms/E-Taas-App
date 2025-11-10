from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from models.sellers import Seller
from models.category import ProductCategory, ServiceCategory
import logging

logger = logging.getLogger(__name__)


async def add_product_category(db: AsyncSession, category_name: str):
    try:
        result = await db.execute(select(ProductCategory).where(ProductCategory.name == category_name))
        existing_category = result.scalar_one_or_none()
        if existing_category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

        new_category = ProductCategory(name=category_name)
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        logger.info(f"Category '{category_name}' added successfully")
        return new_category

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error adding category '{category_name}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def add_service_category(db: AsyncSession, category_name: str):
    try:
        result = await db.execute(select(ServiceCategory).where(ServiceCategory.name == category_name))
        existing_category = result.scalar_one_or_none()
        if existing_category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service category already exists")

        new_category = ServiceCategory(name=category_name)
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        logger.info(f"Service category '{category_name}' added successfully")
        return new_category

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error adding service category '{category_name}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

async def approve_seller(db: AsyncSession, seller_id: int):
    try:
        result = await db.execute(select(Seller).where(Seller.id == seller_id))
        seller = result.scalar_one_or_none()
        if not seller:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        
        if seller.is_verified:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Seller is already verified")
        
        seller.is_verified = True
        await db.commit()
        await db.refresh(seller)
        logger.info(f"Seller ID '{seller_id}' approved successfully")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Seller approved successfully",
                "seller_id": seller.id,
                "is_verified": seller.is_verified
            }
        )
    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error approving seller ID '{seller_id}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")