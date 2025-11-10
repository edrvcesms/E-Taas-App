from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from models.users import User
from models.category import ProductCategory
import logging

logger = logging.getLogger(__name__)


async def add_new_category(db: AsyncSession, category_name: str):
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

