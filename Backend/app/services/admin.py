from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi.responses import JSONResponse
from fastapi import HTTPException, status
from models.sellers import Seller
from models.users import User
from models.category import ProductCategory, ServiceCategory
from schemas.category import ProductCategoryCreate, ServiceCategoryCreate
from schemas.users import UserBase
from services.notification import create_new_notification
from utils.logger import logger


async def add_product_category(db: AsyncSession, category: ProductCategoryCreate):
    try:
        result = await db.execute(select(ProductCategory).where(ProductCategory.category_name == category.category_name))
        logger.info(f"Checking if product category '{category.category_name}' exists")
        existing_category = result.scalar_one_or_none()
        logger.info(f"Existing category found: {existing_category}")
        if existing_category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

        new_category = ProductCategory(category_name=category.category_name)
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)
        logger.info(f"Category '{category.category_name}' added successfully")
        return new_category

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error adding category '{category.category_name}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")

async def add_service_category(db: AsyncSession, category: ServiceCategoryCreate):
    try:
        logger.info(f"Checking if service category '{category.name}' exists")
        result = await db.execute(select(ServiceCategory).where(ServiceCategory.category_name == category.name))
        existing_category = result.scalar_one_or_none()
        logger.info(f"Existing service category found: {existing_category}")
        if existing_category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Service category already exists")

        new_category = ServiceCategory(category_name=category.name)
        db.add(new_category)
        await db.commit()
        await db.refresh(new_category)

        logger.info(f"Service category '{category.name}' added successfully")
        return new_category

    except HTTPException:
        raise

    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error adding service category '{category.name}': {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

async def approve_seller(db: AsyncSession, seller_id: int):
    try:
        logger.info(f"Approving seller for seller ID '{seller_id}'")
        result = await db.execute(select(Seller).where(Seller.id == seller_id))
        seller = result.scalar_one_or_none()
        if not seller:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Seller not found")
        
        result = await db.execute(select(User).where(User.id == seller.user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        seller.is_verified = True
        user.is_seller = True
        await create_new_notification(db, seller_id, "Congratulations! Your application to become a seller has been approved.", role="seller")
        await db.commit()
        await db.refresh(user)
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
    
async def get_sellers_applications(db: AsyncSession):
    try:
        logger.info("Retrieving seller applications")
        result = await db.execute(select(Seller).where(Seller.is_verified == False))
        logger.info(f"Seller applications retrieved: {result}")
        sellers = result.scalars().all()
        return sellers
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error retrieving seller applications: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    

async def get_all_sellers(db: AsyncSession):
    try:
        logger.info("Retrieving all verified sellers")
        result = await db.execute(select(Seller).where(Seller.is_verified == True))
        logger.info(f"All verified sellers retrieved: {result}")
        sellers = result.scalars().all()
        return sellers
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error retrieving all sellers: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
    
async def get_all_users(db: AsyncSession) -> UserBase:
    try:
        logger.info("Retrieving all users")
        result = await db.execute(select(User))
        logger.info(f"All users retrieved: {result}")
        users = result.scalars().all()
        return [UserBase.model_validate(row) for row in users]
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.exception(f"Unexpected error retrieving all users: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")