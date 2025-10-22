from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from schemas.users import SellerInfoUpdate
from models.users import User
from models.category import Category
import logging
from .notification import create_new_notification

logger = logging.getLogger(__name__)


async def add_new_category(db: AsyncSession, category_name: str):
    try:
        result = await db.execute(select(Category).where(Category.name == category_name))
        existing_category = result.scalar_one_or_none()
        if existing_category:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Category already exists")

        new_category = Category(name=category_name)
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


async def update_user_as_seller(db: AsyncSession, user_id: int, seller_info_update_data: SellerInfoUpdate):
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        if user.is_seller:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User is already a seller")

        user.is_seller = True
        for field_name, value in seller_info_update_data.dict(exclude_unset=True).items():
            setattr(user, field_name, value)

        db.add(user)
        await db.commit()
        await db.refresh(user)

        await create_new_notification(db, user_id, "Congratulations! You have been promoted to seller status.")

        logger.info(f"User {user_id} upgraded to seller successfully")
        return user

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        logger.exception(f"Unexpected error upgrading user {user_id} to seller: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error")
