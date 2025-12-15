from core.config import settings
from core.security import hash_password, verify_password, create_access_token, create_refresh_token, decode_token
from models.users import User
from sqlalchemy.orm import selectinload
from schemas.auth import VerifyEmailOTP
from sqlalchemy import select
from fastapi import HTTPException, status, Request
from fastapi.concurrency import run_in_threadpool
from sqlalchemy.ext.asyncio import AsyncSession
from utils.email import send_otp_to_email
from utils.cache import redis_client
from fastapi.responses import JSONResponse
from utils.logger import logger


async def create_admin_user(db: AsyncSession, admin_register_data):
    try:
        logger.info(f"Creating admin user with email: {admin_register_data.email}")
        result = await db.execute(select(User).where(User.email == admin_register_data.email))
        existing_user = result.scalar_one_or_none()
        logger.info(f"Existing user found: {existing_user}")
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
        logger.info(f"Registering user with email: {user_register_data.email}")
        result = await db.execute(select(User).where(User.email == user_register_data.email))
        existing_user = result.scalar_one_or_none()
        logger.info(f"Existing user found: {existing_user}")
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Email already registered"
            )
        try:
            await send_email_verification(db, user_register_data.email)
            logger.info(f"Email verification sent to: {user_register_data.email}")
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content={"message": "An OTP has been sent to your email for verification."}
            )

        except Exception as e:
            logger.error(f"Error sending email verification during registration: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error sending email verification"
            )
        
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Unexpected error during user registration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unexpected error occurred"
        )
    
async def send_email_verification(db: AsyncSession, user_email: str):
    try:
        
        logger.info(f"Sending OTP to email: {user_email}")
        otp = await send_otp_to_email(user_email)

        redis_client.setex(f"email_verification_otp:{user_email}", 300, otp)  # OTP valid for 5 minutes
        logger.info(f"OTP sent to email: {user_email}")

        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "OTP sent to email successfully"}
        )
    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error sending OTP to email {user_email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error sending OTP to email"
        )
    

async def verify_email_otp(db: AsyncSession, verify_data: VerifyEmailOTP):
    try:
        stored_otp = redis_client.get(f"email_verification_otp:{verify_data.email}")
        logger.info(f"Verifying OTP for email: {verify_data.email}")
        if not stored_otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="OTP has expired or is invalid"
            )
        
        if stored_otp != verify_data.otp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid OTP"
            )
        
        redis_client.delete(f"email_verification_otp:{verify_data.email}")
        logger.info(f"OTP verified and deleted for email: {verify_data.email}")
        try:
            hashed_password = await run_in_threadpool(hash_password, verify_data.password)
            new_user = User(
                username=verify_data.username,
                email=verify_data.email,
                hashed_password=hashed_password,
                is_admin=False
            )
            db.add(new_user)
            await db.commit()
            await db.refresh(new_user)
            logger.info(f"Email verified and user created successfully: {verify_data.email}")

        except Exception as e:
            await db.rollback()
            logger.error(f"Error creating user after OTP verification for email {verify_data.email}: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error creating user after OTP verification"
            )
        
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={"message": "Email verified successfully"}
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.error(f"Error verifying OTP for email {verify_data.email}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error verifying OTP"
        )
    
async def login_user(db: AsyncSession, user_login_data):
    try:
        logger.info(f"Logging in user with email: {user_login_data.email}")
        result = await db.execute(select(User).options(selectinload(User.seller)).where(User.email == user_login_data.email))
        user = result.scalar_one_or_none()
        logger.info(f"User found: {user}")
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
        
        result = await db.execute(select(User).options(selectinload(User.seller)).where(User.id == user.id))
        user = result.scalar_one_or_none()

        access_token = create_access_token(data={"user_id": user.id})
        refresh_token = create_refresh_token(data={"user_id": user.id})

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "success": True,
                "message": "Login successful",
                "user": {
                    "id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "middle_name": user.middle_name,
                    "address": user.address,
                    "contact_number": user.contact_number,
                    "is_admin": user.is_admin,
                    "is_seller": user.is_seller,
                    "seller_data": {
                        "id": user.seller.id if user.seller else None,
                        "business_name": user.seller.business_name if user.seller else None,
                        "is_verified": user.seller.is_verified if user.seller else None,
                        "business_address": user.seller.business_address if user.seller else None,
                        "business_contact": user.seller.business_contact if user.seller else None,
                        "display_name": user.seller.display_name if user.seller else None,
                        "owner_address": user.seller.owner_address if user.seller else None
                    } if user.seller else None
                }
            }
        )
        logger.info(f"User logged in successfully: {user.email}")

        await set_cookies(response, access_token, refresh_token)
        
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
    
async def set_cookies(response: JSONResponse, access_token: str, refresh_token: str):
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

   