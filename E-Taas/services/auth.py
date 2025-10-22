from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from fastapi import HTTPException, status
from fastapi.concurrency import run_in_threadpool
from core.security import hash_password, verify_password, create_access_token, create_refresh_token
from models import User
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

async def register_user(db: AsyncSession, user_register_data):
    try:
        result = await db.execute(select(User).where(User.email == user_register_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )

        hashed_password = await run_in_threadpool(hash_password, user_register_data.password)

        new_user = User(
            username=user_register_data.username,
            email=user_register_data.email,
            hashed_password=hashed_password,
        )

        db.add(new_user)

        await db.commit()
        await db.refresh(new_user)

        logger.info(f"User registered successfully: {new_user.email}")

        return {
            "message": "User registered successfully",
            "id": new_user.id,
            "username": new_user.username,
            "email": new_user.email,
        }

    except IntegrityError as e:
        await db.rollback()
        if "duplicate key value" in str(e.orig):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        logger.error(f"Database integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception as e:
        await db.rollback()
        logger.error(f"Unexpected error during registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )
    
async def login_user(db: AsyncSession, user_login_data):
    try:
        result = await db.execute(select(User).where(User.email == user_login_data.email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        if not await run_in_threadpool(verify_password, user_login_data.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})

        logger.info(f"User logged in successfully: {user.email}")

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }
    
    except IntegrityError as e:
        logger.error(f"Database integrity error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error occurred"
        )

    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )
    

