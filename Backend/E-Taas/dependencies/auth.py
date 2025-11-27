from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from models.users import User
from dependencies.database import get_db
from core.security import decode_token, is_token_valid
from core.config import settings
import logging

logger = logging.getLogger(__name__)
bearer_scheme = HTTPBearer()


async def current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    token = request.cookies.get("access_token")
    
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing access token")

    try:
        jwt_payload = decode_token(token, settings.SECRET_KEY, [settings.ALGORITHM])

        if jwt_payload and is_token_valid(token, settings.SECRET_KEY, [settings.ALGORITHM]):
            
            user_id = jwt_payload.get("user_id")
            if not user_id:
                raise HTTPException(status_code=401, detail="Invalid token payload")

            result = await db.execute(
                select(User).options(selectinload(User.sellers)).where(User.id == user_id)
            )
            user = result.scalar_one_or_none()
            if not user:
                raise HTTPException(status_code=404, detail="User not found")
            return user
    except Exception as e:
        logger.warning("JWT token verification failed: %s", e)

    raise HTTPException(status_code=401, detail="Invalid token")
