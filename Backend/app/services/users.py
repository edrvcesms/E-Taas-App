from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from app.models.users import User
from app.schemas.users import UserUpdate
from app.utils.logger import logger
from sqlalchemy.orm import selectinload


async def get_user_by_id(db: AsyncSession, user_id: int):
    try:
        result = await db.execute(select(User).options(selectinload(User.seller)).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return user
    
    except Exception as e:
        logger.exception(f"Error retrieving user {user_id}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

async def update_user_details(db: AsyncSession, user_id: int, user_update_data: UserUpdate):
    try:
        result = await db.execute(select(User).options(selectinload(User.seller)).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        update_values = {field_name: value for field_name, value in user_update_data.dict(exclude_unset=True).items() if value is not None}
        if update_values:
            statement = (
                update(User)
                .where(User.id == user_id)
                .values(**update_values)
                .execution_options(synchronize_session="fetch")
            )
            await db.execute(statement)
            await db.commit()
        
        await db.refresh(user)

        logger.info(f"User {user_id} updated successfully")

        return user
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Error updating user {user_id}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    


async def delete_user(db: AsyncSession, user_id: int) -> None:
    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        await db.delete(user)
        await db.commit()

        logger.info(f"User {user_id} deleted successfully")
    
    except Exception as e:
        await db.rollback()
        logger.exception(f"Error deleting user {user_id}")

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    
    
async def logout_user(request: Request):
    response = JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "success": True,
            "message": "Logout successful"
        }
    )
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
    
