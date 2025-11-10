from core.config import settings
from core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from models.users import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from fastapi import HTTPException, status, Request
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
import logging
from fastapi.responses import JSONResponse
logger = logging.getLogger(__name__)


async def create_admin_user(db: AsyncSession, admin_register_data):
    try:
        result = await db.execute(select(User).where(User.email == admin_register_data.email))
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        
        hashed_password = await run_in_threadpool(hash_password, admin_register_data.password)

        new_admin = User(
            username=admin_register_data.username,
            email=admin_register_data.email,
            hashed_password=hashed_password,
            is_admin=True
        )

        db.add(new_admin)
        await db.commit()
        await db.refresh(new_admin)
        logger.info(f"Admin user created successfully: {new_admin.email}")
        return {
            "message": "Admin user created successfully",
            "id": new_admin.id,
            "username": new_admin.username,
            "email": new_admin.email,
        }
    
    except HTTPException:
        raise
    
    except Exception as e:
        await db.rollback()
        logger.error(f"Error creating admin user: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error creating admin user"
        )

async def register_user(db: AsyncSession, user_register_data):
    try:
        result = await db.execute(select(User).where(User.email == user_register_data.email))
        existing_user = result.scalar_one_or_none()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        try:

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
        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user"
            )

    except HTTPException:
        raise

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

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Login successful",
                "data": {"access_token": access_token, "token_type": "bearer"}
            }
        )

        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            samesite="Lax", # will be changed after deployment
            secure=False, # will be changed after deployment
            expires=30 * 60 # 30 minutes in seconds
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=False, # will be changed after deployment
            samesite="Lax", # will be changed after deployment
            expires=7 * 24 * 60 * 60 # 7 days in seconds
        )
        
        logger.info(f"User logged in successfully: {user.email}")

        return response
    
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error during login: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )

async def token_refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="No refresh token")
    
    payload = decode_token(refresh_token, settings.SECRET_KEY, settings.ALGORITHM)
    
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired refresh token")
    
    
    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token payload"
        )
    
    new_access_token = create_access_token({"user_id": user_id})

    response = JSONResponse({
        "access_token": new_access_token,
        "token_type": "bearer"
    })
    response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            samesite="Lax", # will be changed after deployment
            secure=False, # will be changed after deployment
            expires=30 * 60 # 30 minutes in seconds
        )
    
    return response

   